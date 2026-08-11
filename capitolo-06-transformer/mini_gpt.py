"""Mini-GPT: implementazione completa di un Transformer decoder-only.

Codice del capitolo 6 (Architettura Transformer), assemblato dai sei
listati del libro: configurazione, attention, blocco, modello,
generazione, collaudo.
"""

import math
import torch
from torch import nn
from torch.nn import functional as F
from dataclasses import dataclass


# --- Parte 1: configurazione ---------------------------------------

@dataclass
class ConfigGPT:
    vocab_size: int = 50257   # dimensione del vocabolario
    block_size: int = 1024    # lunghezza massima del contesto
    n_layer:    int = 12      # numero di blocchi impilati
    n_head:     int = 12      # teste di attention per blocco
    n_embd:     int = 768     # dimensione dello stato nascosto
    dropout:    float = 0.1   # frazione di dropout


# --- Parte 2: multi-head attention causale --------------------------

class CausalSelfAttention(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        assert cfg.n_embd % cfg.n_head == 0
        # un'unica proiezione produce Q, K e V concatenati
        self.qkv  = nn.Linear(cfg.n_embd, 3 * cfg.n_embd)
        self.proj = nn.Linear(cfg.n_embd, cfg.n_embd)
        self.n_head = cfg.n_head
        self.drop = nn.Dropout(cfg.dropout)
        # maschera causale triangolare, creata una volta sola
        m = torch.tril(torch.ones(cfg.block_size, cfg.block_size))
        self.register_buffer(
            "maschera", m.view(1, 1, cfg.block_size, cfg.block_size))

    def forward(self, x):
        B, T, C = x.shape          # batch, token, canali
        q, k, v = self.qkv(x).split(C, dim=2)
        # da (B, T, C) a (B, teste, T, C // teste)
        q = q.view(B, T, self.n_head, C // self.n_head).transpose(1, 2)
        k = k.view(B, T, self.n_head, C // self.n_head).transpose(1, 2)
        v = v.view(B, T, self.n_head, C // self.n_head).transpose(1, 2)
        # scaled dot-product attention con maschera causale
        att = (q @ k.transpose(-2, -1)) / math.sqrt(k.size(-1))
        att = att.masked_fill(
            self.maschera[:, :, :T, :T] == 0, float("-inf"))
        att = F.softmax(att, dim=-1)
        y = self.drop(att) @ v
        y = y.transpose(1, 2).contiguous().view(B, T, C)
        return self.proj(y)


# --- Parte 3: feed-forward e blocco Transformer ---------------------

class MLP(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        # espansione a 4x, non linearita', ricompressione
        self.fc   = nn.Linear(cfg.n_embd, 4 * cfg.n_embd)
        self.proj = nn.Linear(4 * cfg.n_embd, cfg.n_embd)
        self.drop = nn.Dropout(cfg.dropout)

    def forward(self, x):
        return self.drop(self.proj(F.gelu(self.fc(x))))


class Blocco(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.ln1 = nn.LayerNorm(cfg.n_embd)
        self.att = CausalSelfAttention(cfg)
        self.ln2 = nn.LayerNorm(cfg.n_embd)
        self.mlp = MLP(cfg)

    def forward(self, x):
        x = x + self.att(self.ln1(x))   # comunicazione tra token
        x = x + self.mlp(self.ln2(x))   # elaborazione per token
        return x


# --- Parte 4: il modello completo ------------------------------------

class MiniGPT(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self.wte = nn.Embedding(cfg.vocab_size, cfg.n_embd)
        self.wpe = nn.Embedding(cfg.block_size, cfg.n_embd)
        self.drop = nn.Dropout(cfg.dropout)
        self.blocchi = nn.ModuleList(
            Blocco(cfg) for _ in range(cfg.n_layer))
        self.ln_f = nn.LayerNorm(cfg.n_embd)
        self.testa = nn.Linear(cfg.n_embd, cfg.vocab_size, bias=False)
        self.testa.weight = self.wte.weight   # weight tying
        self.apply(self._inizializza)

    def _inizializza(self, modulo):
        # inizializzazione in stile GPT-2: pesi piccoli e gaussiani
        if isinstance(modulo, (nn.Linear, nn.Embedding)):
            nn.init.normal_(modulo.weight, mean=0.0, std=0.02)
            if isinstance(modulo, nn.Linear) and modulo.bias is not None:
                nn.init.zeros_(modulo.bias)

    # --- Parte 5: forward pass e generazione -------------------------

    def forward(self, idx, target=None):
        B, T = idx.shape
        pos = torch.arange(T, device=idx.device)
        # embedding dei token + embedding delle posizioni
        x = self.drop(self.wte(idx) + self.wpe(pos))
        for blocco in self.blocchi:
            x = blocco(x)
        x = self.ln_f(x)
        logits = self.testa(x)     # (B, T, vocab_size)
        perdita = None
        if target is not None:
            # cross-entropy su tutte le posizioni insieme
            perdita = F.cross_entropy(
                logits.view(-1, logits.size(-1)), target.view(-1))
        return logits, perdita

    @torch.no_grad()
    def genera(self, idx, max_nuovi, temperatura=1.0, top_k=None):
        for _ in range(max_nuovi):
            # tronca il contesto alla finestra massima
            ctx = idx[:, -self.cfg.block_size:]
            logits, _ = self(ctx)
            logits = logits[:, -1, :]   # solo l'ultima posizione
            if temperatura == 0.0:      # greedy
                prossimo = logits.argmax(dim=-1, keepdim=True)
            else:
                logits = logits / temperatura
                if top_k is not None:   # azzera la coda
                    soglia = torch.topk(logits, top_k).values[:, [-1]]
                    logits[logits < soglia] = float("-inf")
                p = F.softmax(logits, dim=-1)
                prossimo = torch.multinomial(p, num_samples=1)
            idx = torch.cat([idx, prossimo], dim=1)
        return idx


# --- Parte 6: collaudo del modello appena costruito ------------------

if __name__ == "__main__":
    torch.manual_seed(42)
    cfg = ConfigGPT(vocab_size=256, block_size=64,
                    n_layer=4, n_head=4, n_embd=128, dropout=0.0)
    modello = MiniGPT(cfg)

    n_par = sum(p.numel() for p in modello.parameters())
    print(f"parametri: {n_par}")

    # forward su dati casuali: la perdita deve valere circa ln(256)
    x = torch.randint(0, 256, (2, 10))
    t = torch.randint(0, 256, (2, 10))
    logits, perdita = modello(x, t)
    print(f"perdita iniziale: {perdita.item():.4f}"
          f"   attesa: {math.log(256):.4f}")

    # generazione con il modello non addestrato
    modello.eval()
    avvio = torch.zeros(1, 1, dtype=torch.long)
    print(modello.genera(avvio, 8, temperatura=1.0, top_k=40)[0].tolist())
    print(modello.genera(avvio, 8, temperatura=0.0)[0].tolist())

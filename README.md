# NOX Roguelike

Jogo Roguelike desenvolvido em Python com PgZero e POO. Estética Dark Fantasy com movimentação suave em grid e animação de sprites sob os padrões PEP8.

## 📖 Sobre o Projeto

NOX é um roguelike de exploração de dungeons. O jogador controla um mago que deve enfrentar hordas de criaturas através de três níveis progressivamente desafiadores.
O jogo combina mecânicas clássicas de roguelike com sistema de combate dinâmico, incluindo ataques normais e especiais, sistema de stamina e regeneração de vida ao derrotar inimigos.

## 🎮 Funcionalidades

- **Menu Principal Interativo**: Interface com opções de jogar, controles, toggle de música e saída
- **3 Níveis Progressivos**: Dungeons geradas proceduralmente com dificuldade crescente
- **Sistema de Combate**: Ataques corpo a corpo e projéteis especiais com cooldown
- **Variedade de Inimigos**: 7 tipos diferentes de criaturas, incluindo um boss final
- **Animações Fluidas**: Sistema de animação de sprites para movimento, idle e ataques
- **Movimento em Grid**: Deslocamento suave entre células com sistema de câmera
- **Sistema de Stamina**: Barra que recarrega para liberar ataques especiais devastadores
- **Áudio Dinâmico**: Música de fundo e efeitos sonoros com controle de volume
- **Feedback Visual**: Indicadores de dano, barras de HP/Stamina e animações de ataque

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**: Linguagem de programação
- **PgZero**: Framework para desenvolvimento de jogos 2D
- **math**: Cálculos de distância e trajetórias
- **random**: Geração procedural de dungeons e comportamento de inimigos
- **pygame.Rect**: Gerenciamento de colisões e interfaces

## 📋 Pré-requisitos

```bash
Python 3.7+ (pgzero pode ter problemas em python 3.14+)
PgZero
```

## 🚀 Como Instalar e Rodar

1. Clone o repositório:
```bash
git clone https://github.com/maperotto/Nox-Roguelike.git
cd Nox-Roguelike
```

2. Instale as dependências:
```bash
pip install pgzero
```

3. Execute o jogo:
```bash
python jogo.py
```

Ou usando o runner do PgZero:
```bash
pgzrun jogo.py
```

## 🎯 Como Jogar

### Controles

- **Setas / WASD**: Movimentar o personagem
- **Espaço**: Ataque normal (alcance 3 células, dano 30 HP)
- **F**: Ataque especial - Bola de fogo teleguiada (quando stamina estiver cheia)
- **ESC**: Retornar ao menu / Sair do jogo

### Mecânicas

**Objetivo**: Derrote todos os inimigos em cada nível para avançar. Sobreviva aos 3 níveis e derrote o Big Demon para vencer!

**Sistema de Vida**:
- HP inicial: 100
- Regeneração: +10 HP por inimigo morto com ataque normal, +15 HP com ataque especial
- Dano varia conforme o inimigo (10-25 HP)
- Alerta sonoro quando HP cai abaixo de 30%

**Sistema de Stamina**:
- Recarrega automaticamente ao longo do tempo
- Ao encher completamente, libera o ataque especial (tecla F)
- Ataque especial dispara projétil que atravessa múltiplos inimigos

**Inimigos**:
- **Goblin**: Inimigo básico com 70 HP
- **Muddy/Swampy**: Criaturas pantanosas com 70 HP
- **Chort**: Demônio menor com 90 HP e maior dano
- **Masked Orc**: Orc com 70 HP
- **Orc Warrior**: Guerreiro robusto com 150 HP
- **Big Demon (Boss)**: Chefe final com 600 HP e 25 de dano

## 📁 Estrutura do Projeto

```
Projeto Kodland/
│
├── jogo.py                 # Arquivo principal do jogo
├── setup.py                # Script auxiliar para geração de assets
├── reduce_volume.py        # Utilitário para ajuste de volume de sons
├── README.md               # Documentação do projeto
│
├── images/                 # Sprites e imagens
│   ├── sprite_weapon_staff_*.png
│   ├── *_idle_anim_*.png
│   ├── *_run_anim_*.png
│   ├── fireball_*.png
│   └── ...
│
├── sounds/                 # Efeitos sonoros
│   ├── blazing_fire.wav
│   ├── special_attack.wav
│   ├── monster_attack_sound.wav
│   ├── death_sound.wav
│   └── life_sound.wav
│
├── music/                  # Música de fundo
│   └── battle_sound.wav
│
└── Textures/              # Tilesets e recursos gráficos
    └── 0x72_DungeonTilesetII_v1.7/
```

## 🎨 Arquitetura do Código

O jogo utiliza Programação Orientada a Objetos com as seguintes classes principais:

- **Hero**: Classe do personagem jogável com sistema de movimento, ataque e animações
- **Enemy**: Classe base para inimigos com IA simples de perseguição e patrulha
- **Projectile**: Classe para projéteis do ataque especial com sistema de dano único

**Funções principais**:
- `generate_dungeon()`: Geração procedural de salas, corredores e decorações
- `setup_level()`: Configuração de inimigos e estrutura de cada nível
- `draw()`: Renderização de todos os elementos na tela
- `update()`: Loop principal de atualização de lógica e física

## 📝 Padrões de Código

O projeto segue as convenções **PEP8** para Python:
- Nomenclatura clara em inglês para variáveis, funções e classes
- Indentação de 4 espaços
- Separação lógica de funções e classes

## 🎵 Créditos de Assets

- **Tileset**: 0x72 Dungeon Tileset II v1.7
- **Sprites**: Assets customizados e adaptados
- **Sons e Música**: Audio assets diversos


---

# info-sistema-cli

Uma ferramenta de linha de comando desenvolvida em Python que fornece informações detalhadas sobre o sistema operacional e hardware do computador.

## Descrição

O info-sistema-cli é uma interface de linha de comando que permite aos usuários obterem facilmente informações completas sobre seu sistema, incluindo:

- Sistema operacional (nome, versão, arquitetura)
- CPU (núcleos, frequência, utilização)
- Memória (RAM e SWAP)
- Armazenamento (partições, uso de disco)
- Rede (interfaces, estatísticas de I/O)

A ferramenta foi projetada para ser simples de usar, altamente configurável e capaz de apresentar as informações em formato texto estruturado ou JSON, facilitando a integração com outras ferramentas.

## Requisitos

- Python 3.6 ou superior
- Bibliotecas: psutil, tabulate

## Instalação

1. Clone este repositório:
```bash
git clone https://github.com/seu-usuario/info-sistema-cli.git
cd info-sistema-cli
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Torne o script executável (Linux/Mac):
```bash
chmod +x info_sistema.py
```

## Uso

O info-sistema-cli pode ser executado com várias opções para visualizar informações específicas do sistema:

```bash
python info_sistema.py [opções]
```

### Opções disponíveis:

- `--os`: Mostra informações do sistema operacional
- `--cpu`: Mostra informações da CPU
- `--memory`: Mostra informações de memória
- `--disk`: Mostra informações de disco
- `--network`: Mostra informações de rede
- `--all`: Mostra todas as informações
- `--json`: Formata a saída como JSON

### Exemplos

Mostrar todas as informações disponíveis:
```bash
python info_sistema.py --all
```

Mostrar apenas informações de CPU e memória:
```bash
python info_sistema.py --cpu --memory
```

Mostrar informações do sistema operacional em formato JSON:
```bash
python info_sistema.py --os --json
```

## Saída de exemplo

```
==================== OS ====================
Propriedade            Valor
--------------------  ----------------------
system                 Linux
release                5.15.0-1031-azure
version                #38-Ubuntu SMP Mon Feb 6 20:39:20 UTC 2023
architecture           64bit
machine                x86_64
processor              x86_64
hostname               exemplo-servidor
username               usuario
boot_time              2023-04-20 08:15:27

==================== CPU ====================
Propriedade            Valor
--------------------  ----------------------
physical_cores         2
total_cores            4
max_frequency          3500.00MHz
current_frequency      2800.00MHz
total_cpu_usage        12%

Uso de CPU por núcleo:
Core 0: 10.00%
Core 1: 15.00%
Core 2: 8.00%
Core 3: 14.00%
```

## Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.
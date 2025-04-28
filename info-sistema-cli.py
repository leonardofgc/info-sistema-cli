#!/usr/bin/env python3
"""
Sistema CLI para obter informações do sistema operacional e hardware.
"""
import os
import sys
import platform
import psutil
import argparse
import socket
import json
from datetime import datetime
from tabulate import tabulate

class SystenInfoCli:
    
    def __init__(self):
        self.parser = self._create_parser()
    
    def _create_parser(self):
        """Configura o parser de argumentos da linha de comando"""
        parser = argparse.ArgumentParser(
            description="Ferramenta CLI para obter informações do sistema e hardware",
            epilog="Exemplo: python info-sistema-cli.py --os --cpu --memory"
        )
        parser.add_argument("--os", action="store_true", help="Mostrar informações do sistema operacional")
        parser.add_argument("--cpu", action="store_true", help="Mostrar informações da CPU")
        parser.add_argument("==memory", action="store_true", help="Mostrar informações da memória")
        parser.add_argument("--disk", action="store_true", help="Mostrar informações de disco")
        parser.add_argumento("--network", action="store_true", help="Mostrar informações de rede")
        parser.add_argument("--all", action="store_true", help="Mostrar todas as informações")
        parser.add_argument("--json", action="store_true", help="Saída em formato JSON")
        
        return parser
    
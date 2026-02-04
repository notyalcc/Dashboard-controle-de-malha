
import { ChecklistItem, DefensePlan } from './types';

export const APP_VERSION = "1.2.9";

/** 
 * LOGO GRUPO MACOR
 * Prioridade 1: Arquivo local logo.png
 */
export const LOGO_URL = "logo.png"; 

/**
 * LOGO BACKUP (SVG) - Design Profissional de Segurança
 * Escudo com divisas militares, representando proteção e hierarquia.
 */
export const LOGO_SVG_BACKUP = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA0MDAgNTEyIj48ZGVmcz48bGluZWFyR3JhZGllbnQgaWQ9ImEiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMCUiIHkyPSIxMDAlIj48c3RvcCBvZmZzZXQ9IjAlIiBzdG9wLWNvbG9yPSIjMUQzQjZCIi8+PHN0b3Agb2Zmc2V0PSIxMDAlIiBzdG9wLWNvbG9yPSIjMEMyNjQ4Ii8+PC9saW5lYXJHcmFkaWVudD48L2RlZnM+PHBhdGggZD0iTTM1IDMwIGgzMzAgaDAgdjI0MCBjMCAxMzAtMTY1IDIxMi0xNjUgMjEyUzM1IDQwMCAzNSAyNzAgWiIgZmlsbD0idXJsKCNhKSIgc3Ryb2tlPSIjMUQzQjZCIiBzdHJva2Utd2lkdGg9IjgiLz48ZyBmaWxsPSJub25lIiBzdHJva2U9IiNmZmZmZmYiIHN0cm9rZS13aWR0aD0iMjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCI+PHBhdGggZD0iTTEyMCAxNDUgbDgwIDQ1IGw4MC00NSIvPjxwYXRoIGQ9Ik0xMjAgMjA1IGw4MCA0NSBsODAtNDUiLz48cGF0aCBkPSJNMTIwIDI2NSBsODAgNDUgbDgwLTQ1Ii8+PC9nPjxwYXRoIGQ9Ik0zNSA0MGgzMzB2MjMwQzM2NSAzOTAgMjAwIDQ4MCAyMDAgNDgwUzM1IDM5MCAzNSAyNzBaIiBmaWxsPSJub25lIiBzdHJva2U9IiNmZmZmZmYiIHN0cm9rZS13aWR0aD0iNSIgc3Ryb2tlLW9wYWNpdHk9IjAuMiIvPjwvc3ZnPg==";

export const LISTA_POSTOS = [
  "LIDER.", "ENTRADA.", "ENTRADA/LATERAL.", "SAIDA.", "SAIDA/ABASTECIMENTO.",
  "BLINDADO.", "RECEPÇAO.", "COMBOX.", "G.ALTA.", "ESTACIONAMENTO.", "TRIAGEM.",
  "BOLSARIO.", "PAR.", "PAR/P.09.", "DAT.", "G.CEMITERIO.", "RETORNO/P.12.", "SORTER."
];

export const ITENS_VERIFICACAO: ChecklistItem[] = [
  { id: 'armamento', label: "🔫 Armamento", icon: "fa-gun", requiresDetails: true },
  { id: 'colete', label: "🦺 Colete", icon: "fa-vest", requiresDetails: true },
  { id: 'municao', label: "📦 Munição", icon: "fa-box", requiresDetails: true },
  { id: 'radio', label: "📻 Rádio HT (Bateria/Sinal)", icon: "fa-walkie-talkie", requiresDetails: true },
  { id: 'lanterna', label: "🔦 Lanterna", icon: "fa-lightbulb" },
  { id: 'livro', label: "📖 Livro de Ocorrências", icon: "fa-book" },
  { id: 'limpeza', label: "🧹 Limpeza do Posto", icon: "fa-broom" },
  { id: 'detector', label: "🔍 Detector de metal", icon: "fa-magnifying-glass" },
  { id: 'sistema', label: "🖥️ Controle de teste sistema", icon: "fa-desktop" }
];

export const PLANO_DEFESA_TEXTOS: DefensePlan = {
  geral: `**⚠️ PROCEDIMENTO DE INVASÃO**
**Filial 1401 (Duque de Caxias/RJ)**

**1. Não sair da célula de segurança**
* Permaneça protegido na célula.

**2. Acionar dispositivos de segurança**
* Botão de pânico, discador e bollards.

**3. Acionar Central de Monitoramento**
* 📞 (11) 4225 6600 / VOIP 0000 6600

**4. Acionar Polícia Militar**
* 📞 190

**5. Acionar Coordenação/Gerência**
* **Marcio de Carvalho:** 21-99842-0999
* **Valdomiro Santana:** 21-98350-7389
* **André Tavares:** (21) 98523-1900`,
  postos: {
    "Controladora de Acesso (Commbox)": "**Ações Imediatas:**\n* 🚨 **Acionar botão de pânico.**\n* Ao ouvir a sirene: Manter a calma, não se precipitar.\n* 🛡️ **Se abrigar dentro do Blindado.**",
    "Portaria Entrada de Veículos": "**Ações Imediatas:**\n* Ao ouvir a sirene: Manter a calma.\n* 🚫 **Bloquear** qualquer pessoa suspeita e informar o Imediato.\n* 🔒 **Fechar as portas** e se abrigar no corredor atrás do blindado ou na sala da segurança.",
    "Guarita Blindada Pátio Externo": "**Ações Imediatas:**\n* 🚨 **Acionar botão de pânico.**\n* Fazer contato com apoios internos em situação suspeita.\n* 📞 Ligar Central: **(11) 4225-6600 / 94085-4224**.\n* 📞 Ligar para órgãos competentes (190).\n* Auxiliar forças de segurança com localização dos meliantes.\n* Manter rádio/comunicação à vista.\n* Acionar Supervisão Macor.",
    "Recepção de Colaboradores": "**Ações Imediatas:**\n* 🚨 **Acionar botão de pânico.**\n* 🚫 Não entrar em atrito físico.\n* Bloquear suspeitos e informar Imediato.\n* 🏃 **Direcionar pessoas** para dentro da sala de recepção e se abrigar lá.\n* 📞 Ligar Central: **(11) 4225-6600 / 94085-4224**.\n* Orientar sobre posicionamento dos invasores.\n* *Nota: Se possível, bloquear torniquetes para evitar circulação.*",
    "Portaria Saída de Veículos": "**Ações Imediatas:**\n* 🚨 **Acionar botão de pânico** (se houver).\n* Bloquear suspeitos e informar Imediato.\n* 🔒 **Fechar as portas** e se manter abrigado no Blindado.",
    "Vigilante do DAT": "**Ações Imediatas:**\n* Ao ouvir a sirene: Manter a calma.\n* 🚧 **Controlar acesso** dos colaboradores internos.\n* 🛡️ Se abrigar e direcionar colaboradores para o **Mezanino (DAT)**.\n* 📻 Redobrar atenção no Rádio.",
    "Estacionamento Externo": "**Ações Imediatas:**\n* 📻 Informar via Rádio sobre movimentações adversas.\n* 🚗 **Se abrigar atrás dos veículos.**\n* ⚠️ **Se for rendido:** Trocar senha de pânico (conforme combinado) com efetivo interno.",
    "Bolsário e Triagem": "**Ações Imediatas:**\n* 🔒 **Fechar portas Nº 737 e 739** (Bloquear entrada/saída).\n* **Triagem:** Permanecer abrigado no local.\n* **Bolsário:** Orientar colaboradores a permanecerem em **silêncio** no interior do CD (Triagem).\n* 📻 Redobrar atenção no Rádio.",
    "PAR + Ronda Interna": "**Ações Imediatas:**\n* 🚨 **Acionar botão de pânico.**\n* 🔒 **Fechar porta Nº 689**.\n* 🛡️ Manter-se abrigado no PAR e controlar colaboradores internos.\n* 📻 Redobrar atenção no Rádio.",
    "Abastecimento de Loja": "**Ações Imediatas:**\n* 🔒 **Fechar portas Nº 697 (Box Retira) e 315** (próximo à Saída Emergência 14).\n* 🛡️ Manter-se abrigado no Setor.\n* 📻 Redobrar atenção no Rádio.",
    "Conferência da Malha Fina": "**Ações Imediatas:**\n* 🔒 **Fechar porta Nº 264** e todas as abertas.\n* 🛡️ Manter-se abrigado.\n* 🤫 Orientar silêncio total.\n* *Obs: Fora do horário, o fechamento da porta 264 é pelo vigilante do BOLSÁRIO.*",
    "Operadora do Drone": "**Ações Imediatas:**\n* 🚨 **Acionar botão de pânico.**\n* 📞 Ligar Central: **(11) 4225-6600 / 94085-4224**.\n* 🚁 **Sobrevoar perímetro** (se possível) e informar movimentação dos meliantes.\n* Acionar Supervisão Macor.",
    "Vigilante do Sorter": "**Ações Imediatas:**\n* 🔒 **Fechar porta Nº 635.**\n* 🛡️ Controlar colaboradores e orientar a ficarem dentro do Sorter.\n* 📻 Redobrar atenção no Rádio.",
    "Guarita Cemitério": "**Ações Imediatas:**\n* 🚨 **Acionar botão de pânico.**\n* 🚧 **Acionar BOLLARDS e RASGA PNEUS** (imediatamente).\n* Fazer contato com apoios internos em situação suspeita."
  }
};

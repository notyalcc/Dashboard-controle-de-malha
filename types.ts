
export type Status = 'OK' | 'RUIM' | 'N/A';
export type TipoRegistro = 'ENTRADA';
export type NotificationType = 'success' | 'error' | 'info' | 'warning';

export interface User {
  username: string;
  name: string;
  role: string;
  matricula: string;
}

export interface Notification {
  id: string;
  type: NotificationType;
  message: string;
}

export interface ChecklistItem {
  id: string;
  label: string;
  icon: string;
  requiresDetails?: boolean;
}

export interface Submission {
  id: string;
  data_hora: string;
  vigilante_nome: string;
  matricula: string;
  posto: string;
  turno: string;
  tipo_registro: TipoRegistro;
  itens: Record<string, Status>;
  observacoes: string;
  equipamentos_info: string;
  foto?: string;
  assinatura?: string;
  created_at?: string;
}

export interface BroadcastMessage {
  id: number;
  content: string;
  message_type: 'info' | 'warning' | 'error';
  is_active: boolean;
  created_at: string;
}

export interface DefensePlan {
  geral: string;
  postos: Record<string, string>;
}

import { getApiBaseUrl } from "@/infrastructure/api-client";
import type {
  Client,
  DashboardSummary,
  ProcessRow,
} from "@/domain/process";

type SummaryDto = {
  total_processes: number;
  interested_count: number;
  reserved_count: number;
  confirmed_count: number;
  needs_human_count: number;
  total_party_size: number;
  activity_series: { date: string; count: number }[];
};

type ProcessDto = {
  process_id: string;
  client_id: string;
  client_name: string;
  status: ProcessRow["status"];
  party_size: number;
  space_type: ProcessRow["spaceType"];
  received_at: string;
  needs_human: boolean;
};

type ClientDto = {
  id: string;
  name: string;
  phone: string;
};

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${getApiBaseUrl()}${path}`);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export async function fetchDashboardSummary(): Promise<DashboardSummary> {
  const data = await getJson<SummaryDto>("/api/dashboard/summary");
  return {
    totalProcesses: data.total_processes,
    interestedCount: data.interested_count,
    reservedCount: data.reserved_count,
    confirmedCount: data.confirmed_count,
    needsHumanCount: data.needs_human_count,
    totalPartySize: data.total_party_size,
    activitySeries: data.activity_series.map((point) => ({
      date: point.date,
      count: point.count,
    })),
  };
}

export async function fetchProcesses(): Promise<ProcessRow[]> {
  const data = await getJson<ProcessDto[]>("/api/processes");
  return data.map((row) => ({
    processId: row.process_id,
    clientId: row.client_id,
    clientName: row.client_name,
    status: row.status,
    partySize: row.party_size,
    spaceType: row.space_type,
    receivedAt: row.received_at,
    needsHuman: row.needs_human,
  }));
}

export async function fetchClients(): Promise<Client[]> {
  const data = await getJson<ClientDto[]>("/api/clients");
  return data.map((client) => ({
    id: client.id,
    name: client.name,
    phone: client.phone,
  }));
}

export type ProcessStatus = "interested" | "reserved" | "confirmed";
export type SpaceType = "terrace" | "birthday" | "table";

export type ProcessRow = {
  processId: string;
  clientId: string;
  clientName: string;
  status: ProcessStatus;
  partySize: number;
  spaceType: SpaceType;
  receivedAt: string;
  needsHuman: boolean;
};

export type ActivityPoint = {
  date: string;
  count: number;
};

export type DashboardSummary = {
  totalProcesses: number;
  interestedCount: number;
  reservedCount: number;
  confirmedCount: number;
  needsHumanCount: number;
  totalPartySize: number;
  activitySeries: ActivityPoint[];
};

export type Client = {
  id: string;
  name: string;
  phone: string;
};

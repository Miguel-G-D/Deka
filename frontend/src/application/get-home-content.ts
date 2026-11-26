import { createAppInfo, type AppInfo } from "@/domain/app-info";

export function getHomeContent(): AppInfo {
  return createAppInfo("Deka", "Reservations for bars and cafés");
}

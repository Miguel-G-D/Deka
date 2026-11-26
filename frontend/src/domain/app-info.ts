export type AppInfo = {
  name: string;
  tagline: string;
};

export function createAppInfo(name: string, tagline: string): AppInfo {
  return { name, tagline };
}

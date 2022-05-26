/* eslint-disable @typescript-eslint/no-unused-vars */
export interface PlayerData {
  nickname: string;
  character: string;
  skin: string;
  custom_skin: boolean;
  tertiary: string;
  secondary: string;
}

export interface SkinsList {
  [skin: string]: string[];
}

export interface BackgroundsList {
  [skin: string]: number;
}

export interface CharactersList {
  characters: string[];
}

export interface CustomSkin {
  code: string;
  label: string;
}

export interface CustomSkinsList {
  [character: string]: CustomSkin[];
}

export interface Background {
  value: string;
  label: string;
}

export interface TournamentMeta {
  title: string;
  date: string;
  participants: number;
  background: string;
  background_variant: string;
  tournament_url: string;
}

export interface TournamentSettings {
  default_rgb: number[];
  rgb: number[];
  bg_opacity: number;
  layout: number;
}

export interface Top8 {
  1: PlayerData;
  2: PlayerData;
  3: PlayerData;
  4: PlayerData;
  5: PlayerData;
  6: PlayerData;
  7: PlayerData;
  8: PlayerData;
  meta: TournamentMeta;
  settings: TournamentSettings;
}

export interface Social {
  name: string;
  url: string;
  imageUrl: string;
  style: object;
}

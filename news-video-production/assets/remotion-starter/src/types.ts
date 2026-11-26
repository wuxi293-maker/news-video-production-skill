export type Shot = {
  src: string;
  kind: "image" | "video";
  startFrom?: number;
  heading: string;
  body: string;
  highlight?: string;
  source?: string;
};

export type NewsVideoProps = {
  title: string;
  shots: Shot[];
};

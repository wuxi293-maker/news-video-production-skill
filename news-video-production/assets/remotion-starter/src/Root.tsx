import { Composition } from "remotion";
import { NewsVideo } from "./NewsVideo";
import data from "./data.example.json";
import type { NewsVideoProps } from "./types";

const props = data as NewsVideoProps;

export const Root = () => (
  <Composition
    id="NewsVideo"
    component={NewsVideo}
    durationInFrames={props.shots.length * 90}
    fps={30}
    width={1080}
    height={1920}
    defaultProps={props}
  />
);

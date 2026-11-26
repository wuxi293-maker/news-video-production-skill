import { existsSync, mkdirSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";

const target = resolve("public/bgm.wav");
if (existsSync(target)) {
  console.log("BGM already exists at public/bgm.wav");
  process.exit(0);
}

const sampleRate = 44100;
const channels = 2;
const seconds = 12;
const bytesPerSample = 2;
const dataSize = sampleRate * channels * bytesPerSample * seconds;
const buffer = Buffer.alloc(44 + dataSize);

buffer.write("RIFF", 0);
buffer.writeUInt32LE(36 + dataSize, 4);
buffer.write("WAVE", 8);
buffer.write("fmt ", 12);
buffer.writeUInt32LE(16, 16);
buffer.writeUInt16LE(1, 20);
buffer.writeUInt16LE(channels, 22);
buffer.writeUInt32LE(sampleRate, 24);
buffer.writeUInt32LE(sampleRate * channels * bytesPerSample, 28);
buffer.writeUInt16LE(channels * bytesPerSample, 32);
buffer.writeUInt16LE(8 * bytesPerSample, 34);
buffer.write("data", 36);
buffer.writeUInt32LE(dataSize, 40);

mkdirSync(dirname(target), { recursive: true });
writeFileSync(target, buffer);
console.log("Created silent placeholder BGM at public/bgm.wav");

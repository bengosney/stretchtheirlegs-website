import loadEffect, { isEffect } from "./effect";

const _window = window as any;
_window.loadEffect = loadEffect;

if (isEffect(_window.effect)) {
  loadEffect(_window.effect);
}

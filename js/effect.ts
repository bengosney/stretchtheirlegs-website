export interface Effect {
  name: string;
  url: string;
  onload: () => null;
}

export const isEffect = (effect: object | undefined): effect is Effect => {
  if (effect != undefined) {
    return "url" in effect && "name" in effect;
  }

  return false;
};

const loadEffect = (effect: Effect) => {
  if (window.matchMedia && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    const script = document.createElement("script");
    script.src = effect.url;
    script.async = true;
    script.defer = true;
    script.onload = effect.onload;
    document.head.appendChild(script);
    document.body.classList.add(`effect-${effect.name}`);
  }
};

export default loadEffect;

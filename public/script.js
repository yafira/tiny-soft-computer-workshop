// simulates the Tiny Soft Computer as an ambient e-ink display.
// content stays visible for a while, then slowly refreshes.

const content = [
  "you can rest now",
  "you are doing enough",
  "it's okay to slow down",
  "you don't have to earn rest",
  "you are allowed to take up space",
  "this moment is enough",
  "be gentle with yourself today",
  "you are not behind",
  "know when to fold 'em",
  "ready...set...go....",
  "small steps still count",
  "inhale.....exhale.......",
  "you have what you need already",
  "things do come back around",
  "anything can be a poem - even this",
  "you deserve softness too",
  "you are allowed to change your mind",
  "it's okay to ask for help",
  "you don't have to be productive right now",
  "your feelings make sense",
  "you can start again tomorrow",
  "you are worth taking care of",
  "it's okay to not know yet",
  "you can let this be easy",
  "you are allowed to say no",
  "you did not have to be perfect today",
  "this is a good place to pause",
  "you are allowed to feel proud",
  "you can trust yourself here",
  "it's okay to take up less than everything today",
  "you are still growing",

  // expressive faces
  "(^_^)",
  "(._.)",
  "(o_o)",
  "(>_<)",
  "(^.^)",
  "(*_*)",
  "(>.<)",
  "(^o^)",
  "(-_-)",
  "(u_u)",
  "(. .)",
  "(^-^)",

  // tiny sun
  " \\ | /\n-- * --\n / | \\",
];

const screenEl = document.getElementById("screen-text");

if (screenEl) {
  const reduceMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)",
  ).matches;

  let isRefreshing = false;

  // Start with the same simple intro.
  screenEl.textContent = "tiny soft computer";

  function getRandomContent() {
    return content[Math.floor(Math.random() * content.length)];
  }

  function refreshScreen(nextContent) {
    if (isRefreshing) return;

    isRefreshing = true;

    screenEl.classList.add("eink-refresh");

    // Slow, visible e-ink-style refresh.
    const refreshDelay = reduceMotion ? 0 : 500;

    setTimeout(() => {
      screenEl.textContent = nextContent;

      if (reduceMotion) {
        screenEl.classList.remove("eink-refresh");
        isRefreshing = false;
        return;
      }

      setTimeout(() => {
        screenEl.classList.remove("eink-refresh");
        isRefreshing = false;
      }, 450);
    }, refreshDelay);
  }

  function showNextContent() {
    refreshScreen(getRandomContent());
  }

  // Let the intro sit for a moment before the first refresh.
  setTimeout(showNextContent, 5000);

  // Then slowly cycle through the little messages.
  setInterval(showNextContent, 8000);
}

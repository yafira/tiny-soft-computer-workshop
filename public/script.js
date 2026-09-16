// simulates the actual intro sequence + a random reminder,
// mirroring the real device's code.py behavior.
// edit the "reminders" list to match code.py if you change it there.

const reminders = [
  "you can rest now",
  "you are doing enough",
  "it's okay to slow down",
  "you don't have to earn rest",
  "you are allowed to take up space",
  "this moment is enough",
  "be gentle with yourself today",
  "you are not behind",
  "small steps still count",
  "you deserve softness too",
];

const screenEl = document.getElementById("screen-text");

if (screenEl) {
  const sequence = [
    "tiny soft computer",
    "starting up",
    "press the button\nfor a soft reminder",
    () => reminders[Math.floor(Math.random() * reminders.length)],
  ];

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  let i = 0;
  function nextFrame() {
    const frame = sequence[i % sequence.length];
    screenEl.textContent = typeof frame === "function" ? frame() : frame;
    i++;
  }

  if (!reduceMotion) {
    nextFrame();
    setInterval(nextFrame, 2600);
  }
}

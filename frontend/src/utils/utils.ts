import adze, { setup } from 'adze';

function getMode(): 'development' | 'production' | 'preview' {
  const mode = import.meta.env.MODE;

  if (mode === 'development' || mode === 'production' || mode === 'preview') {
    return mode;
  }

  console.error('MODE is not set correctly:', mode);

  return 'production';
}

export const mode = getMode();

setup({
  activeLevel: mode === 'development' ? 'verbose' : 'info',
});

export const logger = adze.withEmoji.timestamp.seal();

import { defineShikiSetup } from '@slidev/types'
import clipsGrammar from '/home/zeerafle/.vscode/extensions/nerg.clips-lang-1.0.4/syntaxes/clips.tmLanguage.json'

export default defineShikiSetup(() => {
  return {
    themes: {
      dark: 'min-dark',
      light: 'min-light',
    },
    langs: [
      'js',
      'typescript',
      'cpp',
      'python',
      'md',
      'html',
      'yaml',
      'vue',
      clipsGrammar
    ],
    transformers: [
      // ...
    ],
  }
})

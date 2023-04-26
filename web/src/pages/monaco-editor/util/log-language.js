function registerLanguage(monaco) {
  monaco.languages.register({
    id: "log"
  });
  monaco.languages.setMonarchTokensProvider("log", {
    tokenizer: {
      root: [
        [/(^[=a-zA-Z].*|\d\s.*)/, "log-normal"],
        [/\sERROR\s.*/, "log-error"],
        [/\sWARN\s.*/, "log-warn"],
        [/\sINFO\s.*/, "log-info"],
        [
          /^([0-9]{4}||[0-9]{2})-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}(.[0-9]{3})?/,
          "log-date",
        ],
        [
          /^[0-9]{2}\/[0-9]{2}\/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}(.[0-9]{3})?/,
          "log-date",
        ],
        [/(^\*\*Waiting queue:.*)/, "log-info"],
        [/(^\*\*result tips:.*)/, "log-info"],
      ],
    },
  });
  monaco.editor.defineTheme("log", {
    base: "vs",
    inherit: true,
    rules: [{
        token: "log-info",
        foreground: "4b71ca"
      },
      {
        token: "log-error",
        foreground: "ff0000",
        fontStyle: "bold"
      },
      {
        token: "log-warn",
        foreground: "FFA500"
      },
      {
        token: "log-date",
        foreground: "008800"
      },
      {
        token: "log-normal",
        foreground: "808080"
      },
    ],
    colors: {
      "editor.lineHighlightBackground": "#ffffff",
      "editorGutter.background": "#f7f7f7",
    },
  });

}

export default registerLanguage;

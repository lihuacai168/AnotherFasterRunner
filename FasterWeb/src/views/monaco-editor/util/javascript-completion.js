import * as monaco from "monaco-editor/esm/vs/editor/editor.api";
// js 有内置提示
function createCompleter(getExtraHints) {
  const createSuggestions = function (model, textUntilPosition) {
    let text = model.getValue();
    textUntilPosition = textUntilPosition.replace(/[*[\]@$()]/g, "").replace(/(\s+|\.)/g, " ");
    let arr = textUntilPosition.split(/[\s;]/);
    let activeStr = arr[arr.length - 1];
    let len = activeStr.length;
    let rexp = new RegExp("([^\\w]|^)" + activeStr + "\\w*", "gim");
    let match = text.match(rexp);
    let mergeHints = Array.from(new Set([...getExtraHints(model)]))
      .sort()
      .filter((ele) => {
        let rexp = new RegExp(ele.substr(0, len), "gim");
        return (match && match.length === 1 && ele === activeStr) || ele.length === 1 ? false : activeStr.match(rexp);
      });
    return mergeHints.map((ele) => ({
      label: ele,
      kind: monaco.languages.CompletionItemKind.Text,
      documentation: ele,
      insertText: ele,
    }));
  };
  return {
    provideCompletionItems(model, position) {
      let textUntilPosition = model.getValueInRange({
        startLineNumber: position.lineNumber,
        startColumn: 1,
        endLineNumber: position.lineNumber,
        endColumn: position.column,
      });
      return { suggestions: createSuggestions(model, textUntilPosition) };
    },
  };
}
export default createCompleter;

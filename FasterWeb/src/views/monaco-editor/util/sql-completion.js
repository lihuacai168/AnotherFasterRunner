import * as monaco from "monaco-editor/esm/vs/editor/editor.api";
const hints = [
  "SELECT",
  "INSERT",
  "DELETE",
  "UPDATE",
  "CREATE TABLE",
  "DROP TABLE",
  "ALTER TABLE",
  "CREATE VIEW",
  "DROP VIEW",
  "CREATE INDEX",
  "DROP INDEX",
  "CREATE PROCEDURE",
  "DROP PROCEDURE",
  "CREATE TRIGGER",
  "DROP TRIGGER",
  "CREATE SCHEMA",
  "DROP SCHEMA",
  "CREATE DOMAIN",
  "ALTER DOMAIN",
  "DROP DOMAIN",
  "GRANT",
  "DENY",
  "REVOKE",
  "COMMIT",
  "ROLLBACK",
  "SET TRANSACTION",
  "DECLARE",
  "EXPLAN",
  "OPEN",
  "FETCH",
  "CLOSE",
  "PREPARE",
  "EXECUTE",
  "DESCRIBE",
  "FORM",
  "ORDER BY",
];
function createCompleter(getExtraHints) {
  const createSuggestions = function (model, textUntilPosition) {
    let text = model.getValue();
    textUntilPosition = textUntilPosition.replace(/[*[\]@$()]/g, "").replace(/(\s+|\.)/g, " ");
    let arr = textUntilPosition.split(/[\s;]/);
    let activeStr = arr[arr.length - 1];
    let len = activeStr.length;
    let rexp = new RegExp("([^\\w]|^)" + activeStr + "\\w*", "gim");
    let match = text.match(rexp);
    let textHints = !match
      ? []
      : match.map((ele) => {
          let rexp = new RegExp(activeStr, "gim");
          let search = ele.search(rexp);
          return ele.substr(search);
        });
    let mergeHints = Array.from(new Set([...hints, ...textHints, ...getExtraHints(model)]))
      .sort()
      .filter((ele) => {
        let rexp = new RegExp(ele.substr(0, len), "gim");
        return (match && match.length === 1 && ele === activeStr) || ele.length === 1 ? false : activeStr.match(rexp);
      });
    return mergeHints.map((ele) => ({
      label: ele,
      kind:
        hints.indexOf(ele) > -1
          ? monaco.languages.CompletionItemKind.Keyword
          : monaco.languages.CompletionItemKind.Text,
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

import * as monaco from 'monaco-editor'
const hints = [
  'SELECT',
  'INSERT',
  'DELETE',
  'UPDATE',
  'CREATE TABLE',
  'DROP TABLE',
  'ALTER TABLE',
  'CREATE VIEW',
  'DROP VIEW',
  'CREATE INDEX',
  'DROP INDEX',
  'CREATE PROCEDURE',
  'DROP PROCEDURE',
  'CREATE TRIGGER',
  'DROP TRIGGER',
  'CREATE SCHEMA',
  'DROP SCHEMA',
  'CREATE DOMAIN',
  'ALTER DOMAIN',
  'DROP DOMAIN',
  'GRANT',
  'DENY',
  'REVOKE',
  'COMMIT',
  'ROLLBACK',
  'SET TRANSACTION',
  'DECLARE',
  'EXPLAN',
  'OPEN',
  'FETCH',
  'CLOSE',
  'PREPARE',
  'EXECUTE',
  'DESCRIBE',
  'FORM',
  'ORDER BY']
function createCompleter(getExtraHints) {
  const createSuggestions = function(model, textUntilPosition) {
    const text = model.getValue()
    textUntilPosition = textUntilPosition.replace(/[\*\[\]@\$\(\)]/g, '').replace(/(\s+|\.)/g, ' ')
    const arr = textUntilPosition.split(/[\s;]/)
    const activeStr = arr[arr.length - 1]
    const len = activeStr.length
    const rexp = new RegExp('([^\\w]|^)' + activeStr + '\\w*', 'gim')
    const match = text.match(rexp)
    const textHints = !match ? []
      : match.map(ele => {
        const rexp = new RegExp(activeStr, 'gim')
        const search = ele.search(rexp)
        return ele.substr(search)
      })
    const mergeHints = Array.from(new Set([...hints, ...textHints, ...getExtraHints(model)]))
      .sort()
      .filter(ele => {
        const rexp = new RegExp(ele.substr(0, len), 'gim')
        return (match && match.length === 1 && ele === activeStr) ||
                    ele.length === 1 ? false : activeStr.match(rexp)
      })
    return mergeHints.map(ele => ({
      label: ele,
      kind: hints.indexOf(ele) > -1
        ? monaco.languages.CompletionItemKind.Keyword
        : monaco.languages.CompletionItemKind.Text,
      documentation: ele,
      insertText: ele
    }))
  }
  return {
    provideCompletionItems(model, position) {
      const textUntilPosition = model.getValueInRange({
        startLineNumber: position.lineNumber,
        startColumn: 1,
        endLineNumber: position.lineNumber,
        endColumn: position.column
      })
      return { suggestions: createSuggestions(model, textUntilPosition) }
    }
  }
}
export default createCompleter

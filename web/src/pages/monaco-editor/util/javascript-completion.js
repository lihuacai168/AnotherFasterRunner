import * as monaco from 'monaco-editor'
// js 有内置提示
function createCompleter(getExtraHints) {
  const createSuggestions = function(model, textUntilPosition) {
    const text = model.getValue()
    textUntilPosition = textUntilPosition.replace(/[\*\[\]@\$\(\)]/g, '').replace(/(\s+|\.)/g, ' ')
    const arr = textUntilPosition.split(/[\s;]/)
    const activeStr = arr[arr.length - 1]
    const len = activeStr.length
    const rexp = new RegExp('([^\\w]|^)' + activeStr + '\\w*', 'gim')
    const match = text.match(rexp)
    const mergeHints = Array.from(new Set([...getExtraHints(model)]))
      .sort()
      .filter(ele => {
        const rexp = new RegExp(ele.substr(0, len), 'gim')
        return (match && match.length === 1 && ele === activeStr) ||
                    ele.length === 1 ? false : activeStr.match(rexp)
      })
    return mergeHints.map(ele => ({
      label: ele,
      kind: monaco.languages.CompletionItemKind.Text,
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

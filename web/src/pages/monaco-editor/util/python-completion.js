import * as monaco from 'monaco-editor'
const hints = [
  // This section is the result of running
  // `for k in keyword.kwlist: print('  "' + k + '",')` in a Python REPL,
  // though note that the output from Python 3 is not a strict superset of the
  // output from Python 2.
  'False', // promoted to keyword.kwlist in Python 3
  'None', // promoted to keyword.kwlist in Python 3
  'True', // promoted to keyword.kwlist in Python 3
  'and',
  'as',
  'assert',
  'async', // new in Python 3
  'await', // new in Python 3
  'break',
  'class',
  'continue',
  'def',
  'del',
  'elif',
  'else',
  'except',
  'exec', // Python 2, but not 3.
  'finally',
  'for',
  'from',
  'global',
  'if',
  'import',
  'in',
  'is',
  'lambda',
  'nonlocal', // new in Python 3
  'not',
  'or',
  'pass',
  'print', // Python 2, but not 3.
  'raise',
  'return',
  'try',
  'while',
  'with',
  'yield',

  'int',
  'float',
  'long',
  'complex',
  'hex',

  'abs',
  'all',
  'any',
  'apply',
  'basestring',
  'bin',
  'bool',
  'buffer',
  'bytearray',
  'callable',
  'chr',
  'classmethod',
  'cmp',
  'coerce',
  'compile',
  'complex',
  'delattr',
  'dict',
  'dir',
  'divmod',
  'enumerate',
  'eval',
  'execfile',
  'file',
  'filter',
  'format',
  'frozenset',
  'getattr',
  'globals',
  'hasattr',
  'hash',
  'help',
  'id',
  'input',
  'intern',
  'isinstance',
  'issubclass',
  'iter',
  'len',
  'locals',
  'list',
  'map',
  'max',
  'memoryview',
  'min',
  'next',
  'object',
  'oct',
  'open',
  'ord',
  'pow',
  'print',
  'property',
  'reversed',
  'range',
  'raw_input',
  'reduce',
  'reload',
  'repr',
  'reversed',
  'round',
  'self',
  'set',
  'setattr',
  'slice',
  'sorted',
  'staticmethod',
  'str',
  'sum',
  'super',
  'tuple',
  'type',
  'unichr',
  'unicode',
  'vars',
  'xrange',
  'zip',

  '__dict__',
  '__methods__',
  '__members__',
  '__class__',
  '__bases__',
  '__name__',
  '__mro__',
  '__subclasses__',
  '__init__',
  '__import__'
]
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

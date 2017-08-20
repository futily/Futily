import { CHEM_STYLE_TYPES } from './constants'

export function getChemType (style) {
  return (
    Object.keys(CHEM_STYLE_TYPES).find(key =>
      CHEM_STYLE_TYPES[key].includes(style)
    ) || 'basic'
  )
}

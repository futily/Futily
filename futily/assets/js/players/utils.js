import { CHEM_STYLE_TYPES } from './constants'

export function getChemType (style) {
  return (
    Object.keys(CHEM_STYLE_TYPES).find(key =>
      CHEM_STYLE_TYPES[key].includes(style)
    ) || 'basic'
  )
}

export function getRatingGradeVariable (rating) {
  const property = `--RatingColor`

  if (rating >= 81) return { property, value: `var(--Color_Great)` }
  else if (rating >= 71) return { property, value: `var(--Color_Good)` }
  else if (rating >= 61) return { property, value: `var(--Color_Average)` }
  else if (rating >= 51) return { property, value: `var(--Color_Fair)` }
  else return { property, value: `var(--Color_Poor)` }
}

export function getPositionGradeVariable (rating) {
  const property = `--RatingColor`

  if (rating >= 90) return { property, value: `var(--Color_Great)` }
  else if (rating >= 80) return { property, value: `var(--Color_Good)` }
  else if (rating >= 70) return { property, value: `var(--Color_Average)` }
  else if (rating >= 60) return { property, value: `var(--Color_Fair)` }
  else return { property, value: `var(--Color_Poor)` }
}

export function getAverageStat ({ players, stat, includeGk = false }) {
  // We might not want the goalkeeper when calculating things like 'pace'
  players = players.filter(player => player.isFilled())

  if (!includeGk) {
    players = players.filter(player => player.index !== 0)
  }

  return Math.round(
    players.reduce((acc, player) => {
      acc += player.isFilled() ? player.data[stat] : 0

      return acc
    }, 0) / players.length || 0
  )
}

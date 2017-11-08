export function getAverageStat ({ players, stat, includeGk = false }) {
  // We might not want the goalkeeper when calculating things like 'pace'
  players = players.filter(player => player.isFilled);

  if (!includeGk) {
    players = players.filter(player => player.index !== 0);
  }
  const playersLength = players.length;
  if (playersLength <= 0) return 0;
  let total = players.reduce((acc, player) => {
    acc += player.isFilled ? player.data[stat] : 0;

    return acc;
  }, 0);
  const average = total / playersLength;

  if (stat === 'rating') {
    players.forEach(player => {
      if (player.data[stat] <= average) return;
      total += player.data[stat] - average;
    });
  }

  return Math.floor(total / playersLength);
}

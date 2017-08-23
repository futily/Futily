export default {
  name: 'PlayerCard',

  props: {
    player: {
      type: Object,
      required: true
    },
    size: {
      type: String,
      default: 'small'
    },
    position: {
      type: String,
      required: false
    }
  },

  render (h) {
    const position = this.position || this.player.position

    return (
      <a
        class={[
          'plyr-Card',
          `plyr-Card-${this.size}`,
          `plyr-Card-${this.player.color}`
        ]}
        href={this.player.url}
      >
        <header class='plyr-Card_Header'>
          <div class='plyr-Card_Meta'>
            <span class='plyr-Card_Rating'>
              {this.player.rating}
            </span>
            <span class='plyr-Card_Position'>
              {position}
            </span>
            <img
              alt=''
              src={`/static/ea-images/clubs/${this.player.club.ea_id}.png`}
              class='plyr-Card_Club'
            />
            <img
              alt=''
              src={`/static/ea-images/nations/${this.player.nation.ea_id}.png`}
              class='plyr-Card_Nation'
            />
          </div>

          <img
            alt=''
            src={`/static/ea-images/players/${this.player.ea_id}.png`}
            class='plyr-Card_Image'
          />
        </header>

        <p class='plyr-Card_Name'>
          {this.player.name}
        </p>

        <div class='plyr-Card_Body'>
          {this.player.stats.map((stat, index) => {
            const key = stat[0]
            const value = stat[1]

            return (
              <div class={['plyr-Card_Stat', `plyr-Card_Stat-${index}`]}>
                <span class='plyr-Card_StatValue'>
                  {value}
                </span>
                <span class='plyr-Card_StatKey'>
                  {key}
                </span>
              </div>
            )
          })}
        </div>
      </a>
    )
  }
}

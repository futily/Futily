<template>
  <PotentialLink :class="['plyr-Card', 'plyr-Card-medium', `plyr-Card-${data.color}`]"
                 :href="isLinked ? data.absolute_url : null"
                 :isLink="isLinked"
                 @click="handleClick">
    <header class="plyr-Card_Header">
      <div class="plyr-Card_Meta">
        <span class="plyr-Card_Rating">{{ data.rating }}</span>
        <span class="plyr-Card_Position">{{ position }}</span>
        <img alt=""
             :src="`/static/ea-images/clubs/${data.club.ea_id}.png`"
             class="plyr-Card_Club">
        <img alt=""
             :src="`/static/ea-images/nations/${data.nation.ea_id}.png`"
             class="plyr-Card_Nation">
      </div>

      <img alt=""
           :src="`/static/ea-images/players/${data.ea_id}.png`"
           class="plyr-Card_Image">
    </header>

    <div class="plyr-Card_Body">
      <p class="plyr-Card_Name">{{ data.name }}</p>

      <div class="plyr-Card_Extra">
        <p class="plyr-Card_Workrates">
          {{ data.work_rate_att[0] }} / {{ data.work_rate_def[0] }}
        </p>
        <p class="plyr-Card_Stars">{{ data.skill_moves }}* SM</p>
        <p class="plyr-Card_Stars">{{ data.weak_foot }}* WF</p>
      </div>

      <div class="plyr-Card_Stats">
        <div :class="['plyr-Card_Stat', `plyr-Card_Stat-${index}`]"
             v-for="([key, value], index) in cardStats">
          <span class="plyr-Card_StatValue">{{ value }}</span>
          <span class="plyr-Card_StatKey">{{ key }}</span>
        </div>
      </div>
    </div>

    <footer class="plyr-Card_Footer" v-if="showChemistry">
      <p class="plyr-Card_Chem">
        Chem:
        <span class="plyr-Card_ChemValue">{{ chemistry }}</span>

        <span class="plyr-Card_ChemBoost" :aria-hidden="isBoosted === false">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 50 50">
            <path d="M24.85 10.126C26.868 5.343 31.478 2 36.84 2c7.223 0 12.425 6.18 13.08 13.544 0 0 .352 1.828-.425 5.12-1.058 4.48-3.545 8.463-6.898 11.502L24.85 48 7.402 32.165c-3.353-3.038-5.84-7.02-6.898-11.503-.777-3.29-.424-5.12-.424-5.12C.734 8.18 5.936 2 13.16 2c5.362 0 9.672 3.343 11.69 8.126z"
                  fill="#C03A2B" />
            <path d="M6 18.078c-.553 0-1-.447-1-1 0-5.514 4.486-10 10-10 .553 0 1 .447 1 1s-.447 1-1 1c-4.41 0-8 3.59-8 8 0 .553-.447 1-1 1z"
                  fill="#ED7161" />
          </svg>
        </span>
      </p>
    </footer>
  </PotentialLink>
</template>

<script>
  import PotentialLink from './PotentialLink';

  export default {
    components: {
      PotentialLink,
    },

    props: {
      chemistry: Number,
      data: Object,
      position: String,
      isBoosted: {
        type: Boolean,
        default: false,
      },
      isLinked: {
        type: Boolean,
        default: false,
      },
      showChemistry: {
        type: Boolean,
        default: false,
      },
    },

    methods: {
      handleClick (evt) {
        if (this.isLinked === false) {
          evt.preventDefault();
        }
      },
    },

    computed: {
      cardStats () {
        const isGk = this.data.is_gk;

        return [
          [isGk ? 'DIV' : 'PAC', this.data.card_att_1],
          [isGk ? 'HAN' : 'SHO', this.data.card_att_2],
          [isGk ? 'KIC' : 'PAS', this.data.card_att_3],
          [isGk ? 'REF' : 'DRI', this.data.card_att_4],
          [isGk ? 'SPD' : 'DEF', this.data.card_att_5],
          [isGk ? 'POS' : 'PHY', this.data.card_att_6],
        ];
      },
    },
  };
</script>

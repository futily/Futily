<template>
  <div class="bld-Slot" @click="handleSlotClick">
    <div class="bld-Slot_Card" v-if="isFilled">
      <PlayerCard :chemistry="player.chemistry.total"
                  :data="player.data"
                  :isBoosted="player.chemistry.boost === 1"
                  :isLinked="isEditable === false"
                  :position="playerPosition"
                  :showChemistry="player.index <= 10" />

      <div class="bld-Slot_Controls" v-if="isEditable">
        <div class="bld-Slot_Control bld-Slot_Control-remove"
             @click.stop="removePlayer({ index: player.index })">
          <span class="bld-Slot_ControlIcon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
              <path d="M425.298 51.358h-91.455V16.696c0-9.22-7.475-16.696-16.696-16.696H194.854c-9.22 0-16.696 7.475-16.696 16.696v34.662H86.703c-9.22 0-16.696 7.475-16.696 16.696v51.357c0 9.22 7.475 16.697 16.696 16.697h338.593c9.22 0 16.696-7.475 16.696-16.696V68.055c0-9.222-7.474-16.696-16.694-16.696zm-124.848 0h-88.9V33.39h88.9V51.36zM93.192 169.497l13.844 326.516c.378 8.937 7.735 15.988 16.68 15.988h264.568c8.945 0 16.302-7.05 16.68-15.988l13.843-326.515H93.192zM205.53 444.105c0 9.22-7.475 16.696-16.696 16.696-9.22 0-16.696-7.474-16.696-16.695V237.39c0-9.22 7.475-16.695 16.696-16.695 9.22 0 16.696 7.475 16.696 16.696v206.715zm67.163 0c0 9.22-7.475 16.696-16.696 16.696s-16.696-7.474-16.696-16.695V237.39c0-9.22 7.476-16.695 16.697-16.695s16.696 7.475 16.696 16.696v206.715zm67.163 0c0 9.22-7.475 16.696-16.696 16.696s-16.696-7.474-16.696-16.695V237.39c0-9.22 7.475-16.695 16.696-16.695s16.696 7.475 16.696 16.696v206.715z" />
            </svg>
          </span>

          <span class="bld-Slot_ControlText">Remove</span>
        </div>

        <div class="bld-Slot_Control bld-Slot_Control-changePosition" @click.stop="cyclePosition">
          <span class="bld-Slot_ControlIcon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 471.475 471.475">
              <path d="M180.25 329.875c-6-4.5-14.4-3.3-18.9 2.7-22.5 29.8-56.8 46.9-94.1 46.9h-37.2c-7.5 0-13.5 6-13.5 13.5s6 13.5 13.5 13.5h37.3c23.1 0 45.2-5.3 65.6-15.7 19.5-9.9 36.8-24.4 50-42 4.4-5.9 3.3-14.4-2.7-18.9zM218.35 140.075c2.5 1.9 5.4 2.8 8.3 2.8 4 0 8-1.8 10.7-5.2 22.5-29 56.4-45.6 93-45.6h78.5l-41.9 41.9c-5.3 5.3-5.3 13.8 0 19.1 2.6 2.6 6.1 4 9.5 4s6.9-1.3 9.5-4l65-65c5.3-5.3 5.3-13.8 0-19.1l-65-65c-5.3-5.3-13.8-5.3-19.1 0-5.3 5.3-5.3 13.8 0 19.1l41.9 41.9h-78.5c-45 0-86.7 20.4-114.4 56.1-4.4 6-3.4 14.4 2.5 19z" />
              <path d="M386.05 318.475c-5.3-5.3-13.8-5.3-19.1 0-5.3 5.3-5.3 13.8 0 19.1l41.9 41.9h-78.5c-64.9 0-117.7-52.8-117.7-117.7v-52c0-79.8-64.9-144.7-144.7-144.7h-37.3c-7.5 0-13.5 6-13.5 13.5s6 13.5 13.5 13.5h37.3c64.9 0 117.7 52.8 117.7 117.7v52c0 79.8 64.9 144.7 144.7 144.7h78.5l-41.9 41.9c-5.3 5.3-5.3 13.8 0 19.1 2.6 2.6 6.1 4 9.5 4s6.9-1.3 9.5-4l65-65c5.3-5.3 5.3-13.8 0-19.1l-64.9-64.9z" />
            </svg>
          </span>

          <span class="bld-Slot_ControlText">Change position</span>
        </div>

        <div class="bld-Slot_Control bld-Slot_Control-toggleLoyalty" @click.stop="toggleLoyalty">
          <span class="bld-Slot_ControlIcon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 50 50">
              <path d="M24.85 10.126C26.868 5.343 31.478 2 36.84 2c7.223 0 12.425 6.18 13.08 13.544 0 0 .352 1.828-.425 5.12-1.058 4.48-3.545 8.463-6.898 11.502L24.85 48 7.402 32.165c-3.353-3.038-5.84-7.02-6.898-11.503-.777-3.29-.424-5.12-.424-5.12C.734 8.18 5.936 2 13.16 2c5.362 0 9.672 3.343 11.69 8.126z"
                    fill="#C03A2B" />
              <path d="M6 18.078c-.553 0-1-.447-1-1 0-5.514 4.486-10 10-10 .553 0 1 .447 1 1s-.447 1-1 1c-4.41 0-8 3.59-8 8 0 .553-.447 1-1 1z"
                    fill="#ED7161" />
            </svg>
          </span>

          <span class="bld-Slot_ControlText">Toggle loyalty</span>
        </div>
      </div>
    </div>

    <span class="bld-Slot_Pedestal"
          v-if="playerIsInTeam">{{ player.positions.fromFormation }}
    </span>
    <input type="hidden"
           name="players"
           :value="`${player.data.id},${player.index},${player.positions.inBuilder},${player.chemistry.total}`"
           v-if="isFilled">
  </div>
</template>

<script>
  import { mapActions, mapGetters, mapMutations } from 'vuex';
  import { playerIsInTeam } from '../utils/utils';

  import PlayerCard from './PlayerCard.vue';
  import * as types from '../types';
  import allowedPositions from '../utils/allowedPositions';
  import { Cycler, getOffsetTop, scrollToY } from '../../utils';

  export default {
    components: {
      PlayerCard,
    },

    props: {
      player: Object,
    },

    data () {
      return {
        positionsCycle: null,
      };
    },

    mounted () {
      if (this.isFilled) {
        this.positionsCycle = this.getPositionsCycle();
      }
    },

    computed: {
      ...mapGetters({
        'formation': types.GET_FORMATION,
        'isEditable': types.GET_IS_EDITABLE,
      }),

      isFilled () {
        return Object.keys(this.player.data).length > 0;
      },

      playerPosition () {
        return this.positionsCycle && this.playerIsInTeam
          ? this.positionsCycle.current
          : this.playerIsInTeam
            ? this.player.positions.fromFormation
            : this.player.data.position;
      },

      playerIsInTeam () {
        return playerIsInTeam(this.player);
      },
    },

    watch: {
      formation () {
        this.positionsCycle = this.getPositionsCycle();
      },

      isFilled () {
        this.positionsCycle = this.getPositionsCycle();
      },
    },

    methods: {
      ...mapActions({
        'removePlayer': types.REMOVE_PLAYER,
      }),

      ...mapMutations({
        'openSearch': types.OPEN_SEARCH,
        'setPlayerPosition': types.SET_PLAYER_POSITION,
        'togglePlayerBoost': types.TOGGLE_PLAYER_BOOST,
      }),

      cyclePosition () {
        this.setPlayerPosition({
          index: this.player.index,
          position: this.positionsCycle.next(),
        });
      },

      getPositionsCycle () {
        if (this.isFilled === false) return null;

        const builderPosition = this.player.positions.inBuilder;
        const playerPosition = this.player.data.position;

        return this.playerIsInTeam
          ? new Cycler({
            items: allowedPositions[builderPosition],
            currentPosition: allowedPositions[builderPosition].indexOf(
              builderPosition,
            ),
          })
          : this.playerIsInTeam === false
            ? new Cycler({
              items: allowedPositions[playerPosition],
              currentPosition: allowedPositions[playerPosition].indexOf(
                playerPosition,
              ),
            })
            : null;
      },

      handleSlotClick () {
        const searchInputY = getOffsetTop(this.$root.$el.querySelector('.bld-Search_Input')) - 20;

        return this.isEditable && window.pageYOffset > searchInputY
          ? scrollToY(searchInputY).then(this.openSearch({ index: this.player.index }))
          : this.isEditable
            ? this.openSearch({ index: this.player.index })
            : null;
      },

      toggleLoyalty () {
        this.togglePlayerBoost({
          index: this.player.index,
        });
      },
    },
  };
</script>

<template>
  <div :class="['bld-Builder_Columns', {'bld-Builder_Columns-share': isEditable === false}]">
    <div class="bld-Builder_Column" v-if="share.url.length > 0">
      <div class="bld-Builder_Share">
        <div class="shr-Bar">
          <ul class="shr-Bar_Items">
            <li class="shr-Bar_Item shr-Bar_Item-twitter">
              <a class="shr-Bar_Share"
                 :href="`https://twitter.com/intent/tweet?url=${share.url}&amp;text=Check out ${title} on Futily! ${share.title}`">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 612 612">
                  <path d="M612 116.258c-22.525 9.98-46.694 16.75-72.088 19.772 25.93-15.527 45.777-40.155 55.184-69.41-24.322 14.378-51.17 24.82-79.775 30.48-22.906-24.438-55.49-39.66-91.63-39.66-69.333 0-125.55 56.218-125.55 125.514 0 9.828 1.11 19.427 3.25 28.606-104.325-5.24-196.834-55.223-258.75-131.174-10.822 18.51-16.98 40.078-16.98 63.1 0 43.56 22.182 81.994 55.836 104.48-20.575-.688-39.926-6.348-56.867-15.756v1.568c0 60.806 43.29 111.554 100.692 123.104-10.517 2.83-21.607 4.398-33.08 4.398-8.107 0-15.947-.803-23.634-2.333 15.985 49.907 62.336 86.2 117.253 87.194-42.946 33.655-97.098 53.656-155.915 53.656-10.134 0-20.116-.612-29.944-1.72 55.568 35.68 121.537 56.484 192.44 56.484 230.947 0 357.187-191.29 357.187-357.188l-.42-16.253C573.87 163.525 595.21 141.42 612 116.257z" />
                </svg>

                <span class="shr-Bar_ShareText">Share {{ title }} on Twitter</span>
              </a>
            </li>

            <li class="shr-Bar_Item shr-Bar_Item-facebook">
              <a class="shr-Bar_Share" :href="`https://www.facebook.com/sharer.php?u=${share.url}`">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96.124 96.123">
                  <path d="M72.09.02L59.623 0C45.62 0 36.57 9.285 36.57 23.656v10.907H24.037c-1.083 0-1.96.878-1.96 1.96v15.804c0 1.083.878 1.96 1.96 1.96H36.57v39.876c0 1.083.877 1.96 1.96 1.96h16.352c1.083 0 1.96-.878 1.96-1.96V54.287h14.654c1.083 0 1.96-.877 1.96-1.96l.006-15.803c0-.52-.207-1.018-.574-1.386-.367-.368-.867-.575-1.387-.575H56.843v-9.246c0-4.444 1.06-6.7 6.848-6.7l8.397-.003c1.082 0 1.96-.878 1.96-1.96V1.98c0-1.08-.877-1.958-1.958-1.96z" />
                </svg>

                <span class="shr-Bar_ShareText">Share {{ title }} on Facebook</span>
              </a>
            </li>

            <li class="shr-Bar_Item shr-Bar_Item-link"></li>
          </ul>
        </div>
      </div>
    </div>

    <div class="bld-Builder_Column">
      <template v-if="isEditable">
        <div class="frm-Form_Items">
          <div class="frm-Form_Item frm-Form_Item-full frm-Form_Item-floatingLabel js-FloatingLabel js-FloatingLabel-active">
            <label class="frm-Form_Label js-FloatingLabel_Label" for="name">
              Formation:
            </label>

            <select class="frm-Form_Select js-FloatingLabel_Input"
                    id="formation"
                    name="formation"
                    @change="updateFormation">
              <option value="">Formations</option>
              <option :value="value"
                      :selected="value === formation"
                      v-for="[value, label] in formationChoices">
                {{ label }}
              </option>
            </select>
          </div>

          <div class="frm-Form_Item frm-Form_Item-full frm-Form_Item-floatingLabel js-FloatingLabel js-FloatingLabel-active">
            <label class="frm-Form_Label js-FloatingLabel_Label" for="title">
              Squad Name:
            </label>

            <input type="text"
                   class="frm-Form_Input js-FloatingLabel_Input"
                   placeholder="Name"
                   name="title"
                   id="title"
                   :value="title"
                   @input="updateTitle" />
          </div>
        </div>

        <div class="bld-Builder_Form">
          <input type="hidden" name="title" :value="title" />
          <input type="hidden" name="page" :value="page" />
          <input type="hidden" name="user" :value="user.id" v-if="user.id > 0" />
          <template v-if="isSbc">
            <input type="hidden" name="sbc" :value="sbcId" />
            <input type="hidden" name="chemistry" :value="stats.chemistry" />
            <input type="hidden" name="rating" :value="stats.rating" />
            <input type="hidden" name="loyalty" :value="boostedPlayersCount" />
            <input type="hidden"
                   name="position_changes"
                   :value="numberOfPlayersWithAPositionChange" />
          </template>

          <button class="bld-Builder_Submit btn-Primary"
                  type="submit"
                  :disabled="isSbc && sbcPassed === false">
            Save squad
          </button>
        </div>
      </template>

      <template v-if="isEditable === false">
        <div class="bld-Builder_KeyValues">
          <div class="bld-Builder_KeyValue">
            <p class="bld-Builder_Key">Name</p>
            <h3 class="bld-Builder_Value">{{ title }}
              <span v-if="user.id > 0"> by
                <a :href="user.link">{{ user.username }}</a>
              </span>
            </h3>
          </div>

          <div class="bld-Builder_KeyValue">
            <p class="bld-Builder_Key">Formation</p>
            <h3 class="bld-Builder_Value">{{ formation }}</h3>
          </div>
        </div>
      </template>
    </div>

    <div class="bld-Builder_Column" v-if="isSbc === false">
      <div class="bld-Builder_Stats">
        <div class="bld-Stats">
          <ul class="bld-Stats_Items">
            <li class="bld-Stats_Item">
              <input type="hidden" name="rating" :value="stats.rating">
              <span class="bld-Stats_Label">Rating:</span>
              <span :class="['bld-Stats_Value', `bld-Stats_Value-${statGrade(stats.rating)}`]">{{ stats.rating }}</span>
            </li>

            <li class="bld-Stats_Item">
              <input type="hidden" name="chemistry" :value="stats.chemistry">
              <span class="bld-Stats_Label">Chemistry:</span>
              <span :class="['bld-Stats_Value', `bld-Stats_Value-${statGrade(stats.chemistry)}`]">{{ stats.chemistry }}</span>
            </li>

            <li class="bld-Stats_Item">
              <span class="bld-Stats_Label">Defensive:</span>
              <span :class="['bld-Stats_Value', `bld-Stats_Value-${statGrade(stats.defensive)}`]">{{ stats.defensive }}</span>
            </li>

            <li class="bld-Stats_Item">
              <span class="bld-Stats_Label">Anchor:</span>
              <span :class="['bld-Stats_Value', `bld-Stats_Value-${statGrade(stats.anchor)}`]">{{ stats.anchor }}</span>
            </li>

            <li class="bld-Stats_Item">
              <span class="bld-Stats_Label">Creative:</span>
              <span :class="['bld-Stats_Value', `bld-Stats_Value-${statGrade(stats.creative)}`]">{{ stats.creative }}</span>
            </li>

            <li class="bld-Stats_Item">
              <span class="bld-Stats_Label">Attacking:</span>
              <span :class="['bld-Stats_Value', `bld-Stats_Value-${statGrade(stats.attacking)}`]">{{ stats.attacking }}</span>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div class="bld-Builder_Column" v-if="isSbc === false">
      <div class="bld-Builder_Stats js-Builder_Stats">
        <div class="bld-Stats">
          <ul class="bld-Stats_Items">
            <li class="bld-Stats_Item">
              <input type="hidden" name="attack" :value="stats.attack">
              <span class="bld-Stats_Label">Attack</span>
              <span :class="['bld-Stats_Value', `bld-Stats_Value-${statGrade(stats.attack)}`]">{{ stats.attack }}</span>
            </li>

            <li class="bld-Stats_Item">
              <input type="hidden" name="midfield" :value="stats.midfield">
              <span class="bld-Stats_Label">Midfield</span>
              <span :class="['bld-Stats_Value', `bld-Stats_Value-${statGrade(stats.midfield)}`]">{{ stats.midfield }}</span>
            </li>

            <li class="bld-Stats_Item">
              <input type="hidden" name="defence" :value="stats.defence">
              <span class="bld-Stats_Label">Defence</span>
              <span :class="['bld-Stats_Value', `bld-Stats_Value-${statGrade(stats.defence)}`]">{{ stats.defence }}</span>
            </li>

            <li class="bld-Stats_Item">
              <input type="hidden" name="pace" :value="stats.pace">
              <span class="bld-Stats_Label">Pace</span>
              <span :class="['bld-Stats_Value', `bld-Stats_Value-${statGrade(stats.pace)}`]">{{ stats.pace }}</span>
            </li>

            <li class="bld-Stats_Item">
              <input type="hidden" name="shooting" :value="stats.shooting">
              <span class="bld-Stats_Label">Shooting</span>
              <span :class="['bld-Stats_Value', `bld-Stats_Value-${statGrade(stats.shooting)}`]">{{ stats.shooting }}</span>
            </li>

            <li class="bld-Stats_Item">
              <input type="hidden" name="passing" :value="stats.passing">
              <span class="bld-Stats_Label">Passing</span>
              <span :class="['bld-Stats_Value', `bld-Stats_Value-${statGrade(stats.passing)}`]">{{ stats.passing }}</span>
            </li>

            <li class="bld-Stats_Item">
              <input type="hidden" name="dribbling" :value="stats.dribbling">
              <span class="bld-Stats_Label">Dribbling</span>
              <span :class="['bld-Stats_Value', `bld-Stats_Value-${statGrade(stats.dribbling)}`]">{{ stats.dribbling }}</span>
            </li>

            <li class="bld-Stats_Item">
              <input type="hidden" name="defending" :value="stats.defending">
              <span class="bld-Stats_Label">Defending</span>
              <span :class="['bld-Stats_Value', `bld-Stats_Value-${statGrade(stats.defending)}`]">{{ stats.defending }}</span>
            </li>

            <li class="bld-Stats_Item">
              <input type="hidden" name="physical" :value="stats.physical">
              <span class="bld-Stats_Label">Physical</span>
              <span :class="['bld-Stats_Value', `bld-Stats_Value-${statGrade(stats.physical)}`]">{{ stats.physical }}</span>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div class="bld-Builder_Column" v-if="isSbc">
      <div class="bld-Builder_Requirements">
        <div class="sbc-Requirements">
          <h4 class="sbc-Requirements_Title">Requirements</h4>

          <ul class="sbc-Requirements_Items">
            <li class="sbc-Requirements_Item" v-for="(requirement, index) in requirements">
              <component :is="getRequirementComponent(requirement)"
                         :index="index"
                         :requirement="requirement"></component>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div class="bld-Builder_Column" v-if="isSbc">
      <div class="bld-Awards">
        <ul class="bld-Awards_Items">
          <li class="bld-Awards_Item" v-for="award in awards">
            <component :is="getAwardComponent(award)" :award="award"></component>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
  import { mapActions, mapGetters, mapMutations } from 'vuex';
  import { debounce } from '../../utils';

  import {
    CoinAward,
    // ItemAward,
    PackAward,
  } from './awards';
  import {
    ChemistryRequirement,
    RatingRequirement,
    ClubRequirement,
    LeagueRequirement,
    NationRequirement,
    RareCountRequirement,
    PlayerCountRequirement,
    SameClubRequirement,
    SameLeagueRequirement,
    SameNationRequirement,
    UniqueClubRequirement,
    UniqueLeagueRequirement,
    UniqueNationRequirement,
  } from './requirements';
  import * as types from '../types';
  import { FORMATION_CHOICES } from '../utils/constants';

  export default {
    components: {
      CoinAward,
      // ItemAward,
      PackAward,

      ChemistryRequirement,
      RatingRequirement,
      ClubRequirement,
      LeagueRequirement,
      NationRequirement,
      RareCountRequirement,
      PlayerCountRequirement,
      SameClubRequirement,
      SameLeagueRequirement,
      SameNationRequirement,
      UniqueClubRequirement,
      UniqueLeagueRequirement,
      UniqueNationRequirement,
    },

    data () {
      return {
        formationChoices: FORMATION_CHOICES,
      };
    },

    computed: {
      ...mapGetters({
        'awards': types.GET_SBC_AWARDS,
        'formation': types.GET_FORMATION,
        'isEditable': types.GET_IS_EDITABLE,
        'isSbc': types.GET_IS_SBC,
        'page': types.GET_PAGE,
        'players': types.GET_PLAYERS,
        'requirements': types.GET_SBC_REQUIREMENTS,
        'sbcId': types.GET_SBC_ID,
        'sbcPassed': types.GET_SBC_PASSED,
        'stats': types.GET_STATS,
        'share': types.GET_SHARE,
        'title': types.GET_TITLE,
        'user': types.GET_USER,
      }),

      boostedPlayersCount () {
        return this.players.team
          .filter(player => player.isFilled)
          .filter(player => player.chemistry.boost === 1)
          .length;
      },

      numberOfPlayersWithAPositionChange () {
        return this.players.team
          .filter(player => player.isFilled)
          .filter(player => player.positions.inBuilder !== player.positions.fromFormation)
          .length;
      },
    },

    methods: {
      ...mapActions({
        'setFormation': types.SET_FORMATION,
      }),

      ...mapMutations({
        'setTitle': types.SET_TITLE,
      }),

      getAwardComponent (award) {
        const { type } = award;

        return {
          'coin': 'CoinAward',
          'item': 'ItemAward',
          'pack': 'PackAward',
        }[type];
      },

      getRequirementComponent (requirement) {
        const { type } = requirement;

        return {
          'chemistry': 'ChemistryRequirement',
          'rating': 'RatingRequirement',
          'club': 'ClubRequirement',
          'league': 'LeagueRequirement',
          'nation': 'NationRequirement',
          'rares': 'RareCountRequirement',
          'player_count': 'PlayerCountRequirement',
          'same_club': 'SameClubRequirement',
          'same_league': 'SameLeagueRequirement',
          'same_nation': 'SameNationRequirement',
          'unique_club': 'UniqueClubRequirement',
          'unique_league': 'UniqueLeagueRequirement',
          'unique_nation': 'UniqueNationRequirement',
        }[type];
      },

      statGrade (val) {
        return val >= 81
          ? 'great'
          : val >= 71
            ? 'good'
            : val >= 61
              ? 'average'
              : val >= 51
                ? 'fair'
                : 'poor';
      },

      updateFormation (evt) {
        this.setFormation({ formation: evt.target.value });
      },

      updateTitle: debounce(function (evt) {
        this.setTitle({ title: evt.target.value });
      }, 300),
    },
  };
</script>

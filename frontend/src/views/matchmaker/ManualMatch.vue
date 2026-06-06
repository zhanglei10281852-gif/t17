<template>
  <div class="manual-match-page">
    <h2>手动牵线</h2>
    <p style="color: #666; margin-bottom: 20px">为会员牵线搭桥，双方将收到推荐通知。</p>

    <a-row :gutter="24">
      <a-col :span="10">
        <a-card title="选择男会员">
          <a-select
            v-model:value="selectedMale"
            placeholder="搜索男会员"
            show-search
            style="width: 100%; margin-bottom: 16px"
            :filter-option="filterOption"
          >
            <a-select-option
              v-for="m in maleMembers"
              :key="m.user_id"
              :value="m.user_id"
            >
              {{ m.nickname }} ({{ m.age }}岁, {{ m.city }})
            </a-select-option>
          </a-select>
          <div v-if="selectedMaleProfile" class="selected-profile">
            <div class="profile-avatar male">
              {{ selectedMaleProfile.nickname?.charAt(0) || '?' }}
            </div>
            <div class="profile-info">
              <h4>{{ selectedMaleProfile.nickname }}</h4>
              <p>{{ selectedMaleProfile.age }}岁 · {{ selectedMaleProfile.city }}</p>
              <p>{{ selectedMaleProfile.occupation }}</p>
            </div>
          </div>
        </a-card>
      </a-col>

      <a-col :span="4" class="middle-col">
        <div class="match-icon">
          <span>💕</span>
          <p>牵线</p>
        </div>
      </a-col>

      <a-col :span="10">
        <a-card title="选择女会员">
          <a-select
            v-model:value="selectedFemale"
            placeholder="搜索女会员"
            show-search
            style="width: 100%; margin-bottom: 16px"
            :filter-option="filterOption"
          >
            <a-select-option
              v-for="f in femaleMembers"
              :key="f.user_id"
              :value="f.user_id"
            >
              {{ f.nickname }} ({{ f.age }}岁, {{ f.city }})
            </a-select-option>
          </a-select>
          <div v-if="selectedFemaleProfile" class="selected-profile">
            <div class="profile-avatar female">
              {{ selectedFemaleProfile.nickname?.charAt(0) || '?' }}
            </div>
            <div class="profile-info">
              <h4>{{ selectedFemaleProfile.nickname }}</h4>
              <p>{{ selectedFemaleProfile.age }}岁 · {{ selectedFemaleProfile.city }}</p>
              <p>{{ selectedFemaleProfile.occupation }}</p>
            </div>
          </div>
        </a-card>
      </a-col>
    </a-row>

    <div class="action-area">
      <a-button type="primary" size="large" :disabled="!canMatch" @click="handleMatch">
        发送牵线通知
      </a-button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import api from '@/utils/request'

const maleMembers = ref([])
const femaleMembers = ref([])
const selectedMale = ref(null)
const selectedFemale = ref(null)

const selectedMaleProfile = computed(() => {
  return maleMembers.value.find(m => m.user_id === selectedMale.value)
})

const selectedFemaleProfile = computed(() => {
  return femaleMembers.value.find(f => f.user_id === selectedFemale.value)
})

const canMatch = computed(() => {
  return selectedMale.value && selectedFemale.value
})

function filterOption(input, option) {
  return option.children.toLowerCase().includes(input.toLowerCase())
}

async function loadMembers() {
  try {
    const [males, females] = await Promise.all([
      api.get('/matchmaker/members?gender=male'),
      api.get('/matchmaker/members?gender=female')
    ])
    maleMembers.value = males
    femaleMembers.value = females
  } catch (e) {
    console.error(e)
  }
}

async function handleMatch() {
  try {
    await api.post('/match/manual', {
      male_user_id: selectedMale.value,
      female_user_id: selectedFemale.value
    })
    message.success('牵线成功，双方已收到通知')
    selectedMale.value = null
    selectedFemale.value = null
  } catch (e) {
    console.error(e)
  }
}

onMounted(() => {
  loadMembers()
})
</script>

<style scoped>
.manual-match-page {
  padding: 0;
}

.manual-match-page h2 {
  margin-top: 0;
}

.middle-col {
  display: flex;
  align-items: center;
  justify-content: center;
}

.match-icon {
  text-align: center;
}

.match-icon span {
  font-size: 48px;
}

.match-icon p {
  margin-top: 8px;
  color: #ff6b6b;
  font-weight: bold;
}

.selected-profile {
  display: flex;
  gap: 16px;
  padding: 16px;
  background: #f9f9f9;
  border-radius: 8px;
}

.profile-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
  font-weight: bold;
  flex-shrink: 0;
}

.profile-avatar.male {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.profile-avatar.female {
  background: linear-gradient(135deg, #f093fb, #f5576c);
}

.profile-info h4 {
  margin: 0 0 4px 0;
}

.profile-info p {
  margin: 4px 0;
  color: #666;
  font-size: 13px;
}

.action-area {
  text-align: center;
  margin-top: 32px;
}
</style>

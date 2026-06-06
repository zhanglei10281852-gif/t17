<template>
  <div class="profile-page">
    <a-card title="个人资料">
      <template #extra>
        <a-tag :color="statusColor[profile?.status]">
          {{ statusMap[profile?.status] }}
        </a-tag>
      </template>

      <a-form
        :model="formState"
        layout="vertical"
        @finish="handleSubmit"
      >
        <a-row :gutter="24">
          <a-col :span="12">
            <a-form-item label="昵称" name="nickname">
              <a-input v-model:value="formState.nickname" placeholder="请输入昵称" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="性别" name="gender">
              <a-select v-model:value="formState.gender" placeholder="请选择性别">
                <a-select-option value="male">男</a-select-option>
                <a-select-option value="female">女</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="24">
          <a-col :span="12">
            <a-form-item label="出生日期" name="birth_date">
              <a-date-picker
                v-model:value="formState.birth_date"
                style="width: 100%"
                :disabled-date="disabledDate"
              />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="身高 (cm)" name="height">
              <a-input-number v-model:value="formState.height" :min="100" :max="250" style="width: 100%" />
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="24">
          <a-col :span="12">
            <a-form-item label="体重 (kg)" name="weight">
              <a-input-number v-model:value="formState.weight" :min="30" :max="200" style="width: 100%" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="学历" name="education">
              <a-select v-model:value="formState.education" placeholder="请选择学历">
                <a-select-option value="high_school">高中</a-select-option>
                <a-select-option value="college">大专</a-select-option>
                <a-select-option value="bachelor">本科</a-select-option>
                <a-select-option value="master">硕士</a-select-option>
                <a-select-option value="doctor">博士</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="24">
          <a-col :span="12">
            <a-form-item label="职业" name="occupation">
              <a-input v-model:value="formState.occupation" placeholder="请输入职业" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="月收入" name="income">
              <a-select v-model:value="formState.income" placeholder="请选择月收入">
                <a-select-option value="below_5k">5k以下</a-select-option>
                <a-select-option value="5k_10k">5-10k</a-select-option>
                <a-select-option value="10k_20k">10-20k</a-select-option>
                <a-select-option value="20k_50k">20-50k</a-select-option>
                <a-select-option value="above_50k">50k以上</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="24">
          <a-col :span="12">
            <a-form-item label="所在城市" name="city">
              <a-input v-model:value="formState.city" placeholder="请输入所在城市" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="户籍地" name="hometown">
              <a-input v-model:value="formState.hometown" placeholder="请输入户籍地" />
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="24">
          <a-col :span="8">
            <a-form-item label="婚姻状况" name="marital_status">
              <a-select v-model:value="formState.marital_status" placeholder="请选择">
                <a-select-option value="single">未婚</a-select-option>
                <a-select-option value="divorced">离异</a-select-option>
                <a-select-option value="widowed">丧偶</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="是否有子女" name="has_children">
              <a-radio-group v-model:value="formState.has_children">
                <a-radio :value="false">否</a-radio>
                <a-radio :value="true">是</a-radio>
              </a-radio-group>
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="是否吸烟" name="smoking">
              <a-radio-group v-model:value="formState.smoking">
                <a-radio :value="false">否</a-radio>
                <a-radio :value="true">是</a-radio>
              </a-radio-group>
            </a-form-item>
          </a-col>
        </a-row>

        <a-form-item label="是否饮酒" name="drinking">
          <a-radio-group v-model:value="formState.drinking">
            <a-radio :value="false">否</a-radio>
            <a-radio :value="true">是</a-radio>
          </a-radio-group>
        </a-form-item>

        <a-form-item label="兴趣爱好" name="hobbies">
          <a-checkbox-group v-model:value="formState.hobbies">
            <a-checkbox value="运动">运动</a-checkbox>
            <a-checkbox value="读书">读书</a-checkbox>
            <a-checkbox value="旅行">旅行</a-checkbox>
            <a-checkbox value="美食">美食</a-checkbox>
            <a-checkbox value="音乐">音乐</a-checkbox>
            <a-checkbox value="电影">电影</a-checkbox>
            <a-checkbox value="游戏">游戏</a-checkbox>
            <a-checkbox value="宠物">宠物</a-checkbox>
            <a-checkbox value="摄影">摄影</a-checkbox>
            <a-checkbox value="烹饪">烹饪</a-checkbox>
          </a-checkbox-group>
        </a-form-item>

        <a-form-item label="自我介绍" name="introduction">
          <a-textarea
            v-model:value="formState.introduction"
            :rows="4"
            placeholder="介绍一下自己吧..."
          />
        </a-form-item>

        <div v-if="profile?.status === 'rejected'" class="reject-reason">
          <a-alert
            message="资料被驳回"
            :description="profile.reject_reason"
            type="warning"
            show-icon
          />
        </div>

        <a-form-item>
          <a-button type="primary" html-type="submit" :loading="submitting">
            保存并提交审核
          </a-button>
          <router-link to="/preference">
            <a-button style="margin-left: 12px">设置择偶条件</a-button>
          </router-link>
        </a-form-item>
      </a-form>
    </a-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import api from '@/utils/request'
import dayjs from 'dayjs'

const profile = ref(null)
const submitting = ref(false)

const statusMap = {
  draft: '草稿',
  pending: '审核中',
  approved: '已通过',
  rejected: '已驳回'
}

const statusColor = {
  draft: 'default',
  pending: 'orange',
  approved: 'green',
  rejected: 'red'
}

const formState = reactive({
  nickname: '',
  gender: undefined,
  birth_date: null,
  height: null,
  weight: null,
  education: undefined,
  occupation: '',
  income: undefined,
  city: '',
  hometown: '',
  marital_status: undefined,
  has_children: false,
  smoking: false,
  drinking: false,
  hobbies: [],
  introduction: ''
})

function disabledDate(current) {
  return current && current > dayjs().endOf('day')
}

async function loadProfile() {
  try {
    const data = await api.get('/profile/me')
    profile.value = data
    formState.nickname = data.nickname || ''
    formState.gender = data.gender
    formState.birth_date = data.birth_date ? dayjs(data.birth_date) : null
    formState.height = data.height
    formState.weight = data.weight
    formState.education = data.education
    formState.occupation = data.occupation || ''
    formState.income = data.income
    formState.city = data.city || ''
    formState.hometown = data.hometown || ''
    formState.marital_status = data.marital_status
    formState.has_children = data.has_children || false
    formState.smoking = data.smoking || false
    formState.drinking = data.drinking || false
    formState.hobbies = data.hobbies || []
    formState.introduction = data.introduction || ''
  } catch (e) {
    console.error(e)
  }
}

async function handleSubmit() {
  submitting.value = true
  try {
    const submitData = { ...formState }
    if (submitData.birth_date) {
      submitData.birth_date = submitData.birth_date.format('YYYY-MM-DD')
    }
    await api.put('/profile/me', submitData)
    message.success('资料已提交审核')
    loadProfile()
  } catch (e) {
    console.error(e)
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  loadProfile()
})
</script>

<style scoped>
.profile-page {
  padding: 24px;
  max-width: 900px;
  margin: 0 auto;
}

.reject-reason {
  margin-bottom: 16px;
}
</style>

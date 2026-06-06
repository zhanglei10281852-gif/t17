<template>
  <div class="activities-manage-page">
    <div class="page-header">
      <h2>活动管理</h2>
      <a-button type="primary" @click="showCreateModal">
        新建活动
      </a-button>
    </div>

    <a-table
      :columns="columns"
      :data-source="activities"
      :loading="loading"
      :pagination="{ pageSize: 10 }"
      row-key="id"
    >
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'status'">
          <a-tag :color="statusColor[record.status]">
            {{ statusMap[record.status] }}
          </a-tag>
        </template>
        <template v-else-if="column.key === 'type'">
          {{ typeMap[record.activity_type] }}
        </template>
        <template v-else-if="column.key === 'time'">
          {{ formatDateTime(record.activity_time) }}
        </template>
        <template v-else-if="column.key === 'quota'">
          男 {{ record.male_registered }}/{{ record.male_limit }}
          <br />
          女 {{ record.female_registered }}/{{ record.female_limit }}
        </template>
        <template v-else-if="column.key === 'action'">
          <a-space>
            <a-button size="small" @click="editActivity(record)">编辑</a-button>
            <a-button size="small" @click="viewParticipants(record)">参与者</a-button>
          </a-space>
        </template>
      </template>
    </a-table>

    <a-modal
      v-model:open="modalVisible"
      :title="editingActivity ? '编辑活动' : '新建活动'"
      width="600px"
      @ok="handleSubmit"
      @cancel="modalVisible = false"
      :confirm-loading="submitting"
    >
      <a-form :model="formState" layout="vertical">
        <a-form-item label="活动名称" required>
          <a-input v-model:value="formState.name" placeholder="请输入活动名称" />
        </a-form-item>
        <a-row :gutter="12">
          <a-col :span="12">
            <a-form-item label="活动时间" required>
              <a-date-picker
                v-model:value="formState.activity_time"
                show-time
                style="width: 100%"
                format="YYYY-MM-DD HH:mm"
              />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="活动形式" required>
              <a-select v-model:value="formState.activity_type" placeholder="请选择">
                <a-select-option value="eight_minute">8分钟约会</a-select-option>
                <a-select-option value="outdoor">户外联谊</a-select-option>
                <a-select-option value="theme_party">主题派对</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>
        <a-form-item label="活动地点" required>
          <a-input v-model:value="formState.location" placeholder="请输入活动地点" />
        </a-form-item>
        <a-row :gutter="12">
          <a-col :span="8">
            <a-form-item label="男性名额" required>
              <a-input-number v-model:value="formState.male_limit" :min="1" style="width: 100%" />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="女性名额" required>
              <a-input-number v-model:value="formState.female_limit" :min="1" style="width: 100%" />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="活动费用 (元)">
              <a-input-number v-model:value="formState.fee" :min="0" style="width: 100%" />
            </a-form-item>
          </a-col>
        </a-row>
        <a-row :gutter="12">
          <a-col :span="12">
            <a-form-item label="最小年龄">
              <a-input-number v-model:value="formState.min_age" :min="18" style="width: 100%" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="最大年龄">
              <a-input-number v-model:value="formState.max_age" :min="18" style="width: 100%" />
            </a-form-item>
          </a-col>
        </a-row>
        <a-form-item label="活动状态">
          <a-select v-model:value="formState.status">
            <a-select-option value="registering">报名中</a-select-option>
            <a-select-option value="full">已满员</a-select-option>
            <a-select-option value="ongoing">进行中</a-select-option>
            <a-select-option value="ended">已结束</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="活动描述">
          <a-textarea
            v-model:value="formState.description"
            :rows="3"
            placeholder="请输入活动描述"
          />
        </a-form-item>
      </a-form>
    </a-modal>

    <a-modal
      v-model:open="participantsVisible"
      title="活动参与者"
      width="700px"
      :footer="null"
    >
      <a-table
        :columns="participantColumns"
        :data-source="participants"
        :loading="participantsLoading"
        :pagination="{ pageSize: 10 }"
        row-key="id"
        size="small"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'name'">
            {{ record.user_profile?.nickname }}
          </template>
          <template v-else-if="column.key === 'gender'">
            {{ record.user_profile?.gender === 'male' ? '男' : '女' }}
          </template>
          <template v-else-if="column.key === 'age'">
            {{ record.user_profile?.age }}岁
          </template>
          <template v-else-if="column.key === 'city'">
            {{ record.user_profile?.city }}
          </template>
        </template>
      </a-table>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import api from '@/utils/request'
import dayjs from 'dayjs'

const activities = ref([])
const loading = ref(false)
const modalVisible = ref(false)
const editingActivity = ref(null)
const submitting = ref(false)
const participantsVisible = ref(false)
const participants = ref([])
const participantsLoading = ref(false)

const statusMap = {
  registering: '报名中',
  full: '已满员',
  ongoing: '进行中',
  ended: '已结束'
}

const statusColor = {
  registering: 'green',
  full: 'orange',
  ongoing: 'blue',
  ended: 'default'
}

const typeMap = {
  eight_minute: '8分钟约会',
  outdoor: '户外联谊',
  theme_party: '主题派对'
}

const columns = [
  { title: '活动名称', dataIndex: 'name', key: 'name' },
  { title: '活动形式', key: 'type', width: 100 },
  { title: '活动时间', key: 'time', width: 160 },
  { title: '地点', dataIndex: 'location', key: 'location', ellipsis: true },
  { title: '名额', key: 'quota', width: 120 },
  { title: '费用', dataIndex: 'fee', key: 'fee', width: 80 },
  { title: '状态', key: 'status', width: 100 },
  { title: '操作', key: 'action', width: 140 }
]

const participantColumns = [
  { title: '昵称', key: 'name' },
  { title: '性别', key: 'gender', width: 60 },
  { title: '年龄', key: 'age', width: 60 },
  { title: '城市', key: 'city' }
]

const formState = reactive({
  name: '',
  activity_time: null,
  activity_type: undefined,
  location: '',
  male_limit: 10,
  female_limit: 10,
  min_age: 18,
  max_age: 60,
  fee: 0,
  status: 'registering',
  description: ''
})

function formatDateTime(dt) {
  return dayjs(dt).format('YYYY-MM-DD HH:mm')
}

async function loadActivities() {
  loading.value = true
  try {
    const data = await api.get('/activities')
    activities.value = data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function showCreateModal() {
  editingActivity.value = null
  Object.assign(formState, {
    name: '',
    activity_time: null,
    activity_type: undefined,
    location: '',
    male_limit: 10,
    female_limit: 10,
    min_age: 18,
    max_age: 60,
    fee: 0,
    status: 'registering',
    description: ''
  })
  modalVisible.value = true
}

function editActivity(record) {
  editingActivity.value = record
  Object.assign(formState, {
    name: record.name,
    activity_time: dayjs(record.activity_time),
    activity_type: record.activity_type,
    location: record.location,
    male_limit: record.male_limit,
    female_limit: record.female_limit,
    min_age: record.min_age,
    max_age: record.max_age,
    fee: record.fee,
    status: record.status,
    description: record.description
  })
  modalVisible.value = true
}

async function handleSubmit() {
  submitting.value = true
  try {
    const submitData = { ...formState }
    if (submitData.activity_time) {
      submitData.activity_time = submitData.activity_time.format('YYYY-MM-DD HH:mm:ss')
    }
    
    if (editingActivity.value) {
      await api.put(`/activities/${editingActivity.value.id}`, submitData)
      message.success('更新成功')
    } else {
      await api.post('/activities', submitData)
      message.success('创建成功')
    }
    modalVisible.value = false
    loadActivities()
  } catch (e) {
    console.error(e)
  } finally {
    submitting.value = false
  }
}

async function viewParticipants(record) {
  participantsVisible.value = true
  participantsLoading.value = true
  try {
    const data = await api.get(`/activities/${record.id}/participants`)
    participants.value = data
  } catch (e) {
    console.error(e)
  } finally {
    participantsLoading.value = false
  }
}

onMounted(() => {
  loadActivities()
})
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
}

.activities-manage-page {
  padding: 0;
}
</style>

<template>
  <div class="profile-review-page">
    <h2>资料审核</h2>

    <a-table
      :columns="columns"
      :data-source="profiles"
      :loading="loading"
      :pagination="{ pageSize: 10 }"
      row-key="id"
    >
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'avatar'">
          <div class="avatar-cell" :class="record.gender === 'male' ? 'male' : 'female'">
            {{ record.nickname?.charAt(0) || '?' }}
          </div>
        </template>
        <template v-else-if="column.key === 'status'">
          <a-tag :color="statusColor[record.status]">
            {{ statusMap[record.status] }}
          </a-tag>
        </template>
        <template v-else-if="column.key === 'action'">
          <a-button type="primary" size="small" @click="viewDetail(record)">
            查看审核
          </a-button>
        </template>
      </template>
    </a-table>

    <a-modal
      v-model:open="detailVisible"
      title="资料详情"
      width="700px"
      :footer="null"
    >
      <div v-if="currentProfile" class="profile-detail">
        <div class="detail-header">
          <div class="detail-avatar" :class="currentProfile.gender === 'male' ? 'male' : 'female'">
            {{ currentProfile.nickname?.charAt(0) || '?' }}
          </div>
          <div class="detail-title">
            <h3>{{ currentProfile.nickname }}</h3>
            <a-tag :color="statusColor[currentProfile.status]">
              {{ statusMap[currentProfile.status] }}
            </a-tag>
          </div>
        </div>

        <a-descriptions :column="2" bordered size="small">
          <a-descriptions-item label="性别">
            {{ currentProfile.gender === 'male' ? '男' : '女' }}
          </a-descriptions-item>
          <a-descriptions-item label="年龄">{{ currentProfile.age }}岁</a-descriptions-item>
          <a-descriptions-item label="身高">{{ currentProfile.height }}cm</a-descriptions-item>
          <a-descriptions-item label="体重">{{ currentProfile.weight }}kg</a-descriptions-item>
          <a-descriptions-item label="学历">{{ educationMap[currentProfile.education] }}</a-descriptions-item>
          <a-descriptions-item label="职业">{{ currentProfile.occupation }}</a-descriptions-item>
          <a-descriptions-item label="月收入">{{ incomeMap[currentProfile.income] }}</a-descriptions-item>
          <a-descriptions-item label="所在城市">{{ currentProfile.city }}</a-descriptions-item>
          <a-descriptions-item label="户籍地">{{ currentProfile.hometown }}</a-descriptions-item>
          <a-descriptions-item label="婚姻状况">
            {{ maritalMap[currentProfile.marital_status] }}
          </a-descriptions-item>
          <a-descriptions-item label="是否有子女">
            {{ currentProfile.has_children ? '是' : '否' }}
          </a-descriptions-item>
          <a-descriptions-item label="是否吸烟">
            {{ currentProfile.smoking ? '是' : '否' }}
          </a-descriptions-item>
          <a-descriptions-item label="是否饮酒">
            {{ currentProfile.drinking ? '是' : '否' }}
          </a-descriptions-item>
          <a-descriptions-item label="兴趣爱好" :span="2">
            <a-tag v-for="hobby in currentProfile.hobbies" :key="hobby" color="pink">
              {{ hobby }}
            </a-tag>
          </a-descriptions-item>
          <a-descriptions-item label="自我介绍" :span="2">
            {{ currentProfile.introduction }}
          </a-descriptions-item>
        </a-descriptions>

        <div v-if="currentProfile.status === 'pending'" class="review-actions">
          <a-input-textarea
            v-model:value="rejectReason"
            placeholder="驳回原因（仅驳回时填写）"
            :rows="3"
            style="margin-bottom: 12px"
          />
          <div class="actions">
            <a-button type="primary" @click="approveProfile">通过</a-button>
            <a-button danger @click="rejectProfile">驳回</a-button>
          </div>
        </div>
      </div>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import api from '@/utils/request'

const profiles = ref([])
const loading = ref(false)
const detailVisible = ref(false)
const currentProfile = ref(null)
const rejectReason = ref('')

const statusMap = {
  draft: '草稿',
  pending: '待审核',
  approved: '已通过',
  rejected: '已驳回'
}

const statusColor = {
  draft: 'default',
  pending: 'orange',
  approved: 'green',
  rejected: 'red'
}

const educationMap = {
  high_school: '高中',
  college: '大专',
  bachelor: '本科',
  master: '硕士',
  doctor: '博士'
}

const incomeMap = {
  below_5k: '5k以下',
  '5k_10k': '5-10k',
  '10k_20k': '10-20k',
  '20k_50k': '20-50k',
  above_50k: '50k以上'
}

const maritalMap = {
  single: '未婚',
  divorced: '离异',
  widowed: '丧偶'
}

const columns = [
  { title: '头像', key: 'avatar', width: 80 },
  { title: '昵称', dataIndex: 'nickname', key: 'nickname' },
  { title: '性别', dataIndex: 'gender', key: 'gender', width: 80 },
  { title: '年龄', dataIndex: 'age', key: 'age', width: 80 },
  { title: '城市', dataIndex: 'city', key: 'city', width: 100 },
  { title: '状态', key: 'status', width: 100 },
  { title: '操作', key: 'action', width: 120 }
]

async function loadProfiles() {
  loading.value = true
  try {
    const data = await api.get('/profile/matchmaker/pending')
    profiles.value = data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function viewDetail(record) {
  currentProfile.value = record
  rejectReason.value = ''
  detailVisible.value = true
}

async function approveProfile() {
  try {
    await api.post(`/profile/matchmaker/review/${currentProfile.value.id}`, {
      status: 'approved'
    })
    message.success('审核通过')
    detailVisible.value = false
    loadProfiles()
  } catch (e) {
    console.error(e)
  }
}

async function rejectProfile() {
  if (!rejectReason.value.trim()) {
    message.warning('请填写驳回原因')
    return
  }
  try {
    await api.post(`/profile/matchmaker/review/${currentProfile.value.id}`, {
      status: 'rejected',
      reject_reason: rejectReason.value
    })
    message.success('已驳回')
    detailVisible.value = false
    loadProfiles()
  } catch (e) {
    console.error(e)
  }
}

onMounted(() => {
  loadProfiles()
})
</script>

<style scoped>
.profile-review-page h2 {
  margin-top: 0;
  margin-bottom: 20px;
}

.avatar-cell {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
}

.avatar-cell.male { background: linear-gradient(135deg, #667eea, #764ba2); }
.avatar-cell.female { background: linear-gradient(135deg, #f093fb, #f5576c); }

.profile-detail {
  padding: 10px 0;
}

.detail-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.detail-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 28px;
  font-weight: bold;
}

.detail-avatar.male { background: linear-gradient(135deg, #667eea, #764ba2); }
.detail-avatar.female { background: linear-gradient(135deg, #f093fb, #f5576c); }

.detail-title h3 {
  margin: 0 0 8px 0;
}

.review-actions {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
}

.review-actions .actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>

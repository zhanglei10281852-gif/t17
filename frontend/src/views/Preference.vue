<template>
  <div class="preference-page">
    <a-card title="择偶条件">
      <a-form
        :model="formState"
        layout="vertical"
        @finish="handleSubmit"
      >
        <a-row :gutter="24">
          <a-col :span="12">
            <a-form-item label="最小年龄" name="min_age">
              <a-input-number v-model:value="formState.min_age" :min="18" :max="60" style="width: 100%" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="最大年龄" name="max_age">
              <a-input-number v-model:value="formState.max_age" :min="18" :max="80" style="width: 100%" />
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="24">
          <a-col :span="12">
            <a-form-item label="最低身高 (cm)" name="min_height">
              <a-input-number v-model:value="formState.min_height" :min="100" :max="250" style="width: 100%" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="最高身高 (cm)" name="max_height">
              <a-input-number v-model:value="formState.max_height" :min="100" :max="250" style="width: 100%" />
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="24">
          <a-col :span="12">
            <a-form-item label="最低学历" name="min_education">
              <a-select v-model:value="formState.min_education" placeholder="请选择最低学历">
                <a-select-option value="high_school">高中</a-select-option>
                <a-select-option value="college">大专</a-select-option>
                <a-select-option value="bachelor">本科</a-select-option>
                <a-select-option value="master">硕士</a-select-option>
                <a-select-option value="doctor">博士</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="最低收入" name="min_income">
              <a-select v-model:value="formState.min_income" placeholder="请选择最低收入">
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
            <a-form-item label="是否接受离异" name="accept_divorced">
              <a-radio-group v-model:value="formState.accept_divorced">
                <a-radio :value="true">接受</a-radio>
                <a-radio :value="false">不接受</a-radio>
              </a-radio-group>
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="是否接受有子女" name="accept_with_children">
              <a-radio-group v-model:value="formState.accept_with_children">
                <a-radio :value="true">接受</a-radio>
                <a-radio :value="false">不接受</a-radio>
              </a-radio-group>
            </a-form-item>
          </a-col>
        </a-row>

        <a-form-item label="偏好城市" name="preferred_cities">
          <a-select
            v-model:value="formState.preferred_cities"
            mode="tags"
            placeholder="输入城市名后按回车添加"
            style="width: 100%"
          >
            <a-select-option value="北京">北京</a-select-option>
            <a-select-option value="上海">上海</a-select-option>
            <a-select-option value="广州">广州</a-select-option>
            <a-select-option value="深圳">深圳</a-select-option>
            <a-select-option value="杭州">杭州</a-select-option>
            <a-select-option value="成都">成都</a-select-option>
            <a-select-option value="武汉">武汉</a-select-option>
            <a-select-option value="南京">南京</a-select-option>
            <a-select-option value="西安">西安</a-select-option>
            <a-select-option value="重庆">重庆</a-select-option>
          </a-select>
        </a-form-item>

        <a-form-item>
          <a-button type="primary" html-type="submit" :loading="submitting">
            保存择偶条件
          </a-button>
          <router-link to="/profile">
            <a-button style="margin-left: 12px">返回个人资料</a-button>
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

const submitting = ref(false)

const formState = reactive({
  min_age: 20,
  max_age: 40,
  min_height: 150,
  max_height: 200,
  min_education: 'high_school',
  min_income: 'below_5k',
  accept_divorced: true,
  accept_with_children: true,
  preferred_cities: []
})

async function loadPreference() {
  try {
    const data = await api.get('/profile/preference/me')
    formState.min_age = data.min_age
    formState.max_age = data.max_age
    formState.min_height = data.min_height
    formState.max_height = data.max_height
    formState.min_education = data.min_education
    formState.min_income = data.min_income
    formState.accept_divorced = data.accept_divorced
    formState.accept_with_children = data.accept_with_children
    formState.preferred_cities = data.preferred_cities || []
  } catch (e) {
    console.error(e)
  }
}

async function handleSubmit() {
  submitting.value = true
  try {
    await api.put('/profile/preference/me', formState)
    message.success('择偶条件已保存')
  } catch (e) {
    console.error(e)
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  loadPreference()
})
</script>

<style scoped>
.preference-page {
  padding: 24px;
  max-width: 900px;
  margin: 0 auto;
}
</style>

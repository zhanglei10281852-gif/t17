<template>
  <div class="register-container">
    <a-card class="register-card" :bordered="false">
      <div class="register-header">
        <h1>💕 注册账号</h1>
        <p>开启你的缘分之旅</p>
      </div>
      <a-form
        :model="formState"
        @finish="handleRegister"
        layout="vertical"
      >
        <a-form-item
          label="手机号"
          name="phone"
          :rules="[{ required: true, message: '请输入手机号' }]"
        >
          <a-input
            v-model:value="formState.phone"
            placeholder="请输入手机号"
            size="large"
          />
        </a-form-item>
        <a-form-item
          label="密码"
          name="password"
          :rules="[
            { required: true, message: '请输入密码' },
            { min: 6, message: '密码至少6位' }
          ]"
        >
          <a-input-password
            v-model:value="formState.password"
            placeholder="请输入密码"
            size="large"
          />
        </a-form-item>
        <a-form-item
          label="确认密码"
          name="confirmPassword"
          :rules="[
            { required: true, message: '请确认密码' },
            { validator: checkPassword }
          ]"
        >
          <a-input-password
            v-model:value="formState.confirmPassword"
            placeholder="请再次输入密码"
            size="large"
          />
        </a-form-item>
        <a-form-item>
          <a-button type="primary" html-type="submit" size="large" block :loading="loading">
            注册
          </a-button>
        </a-form-item>
        <div class="register-footer">
          <span>已有账号？</span>
          <router-link to="/login">立即登录</router-link>
        </div>
      </a-form>
    </a-card>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)

const formState = reactive({
  phone: '',
  password: '',
  confirmPassword: ''
})

function checkPassword(_rule, value) {
  if (value !== formState.password) {
    return Promise.reject('两次密码不一致')
  }
  return Promise.resolve()
}

async function handleRegister() {
  loading.value = true
  try {
    await userStore.register(formState.phone, formState.password)
    message.success('注册成功')
    router.push('/profile')
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
  padding: 20px;
}

.register-card {
  width: 100%;
  max-width: 420px;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
}

.register-header {
  text-align: center;
  margin-bottom: 32px;
}

.register-header h1 {
  font-size: 28px;
  color: #333;
  margin-bottom: 8px;
}

.register-header p {
  color: #999;
  font-size: 14px;
}

.register-footer {
  text-align: center;
  font-size: 14px;
  color: #666;
}

.register-footer a {
  color: #ff6b6b;
  text-decoration: none;
  margin-left: 4px;
}
</style>

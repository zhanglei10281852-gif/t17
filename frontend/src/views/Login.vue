<template>
  <div class="login-container">
    <a-card class="login-card" :bordered="false">
      <div class="login-header">
        <h1>💕 相亲平台</h1>
        <p>遇见你，遇见爱</p>
      </div>
      <a-form
        :model="formState"
        @finish="handleLogin"
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
          :rules="[{ required: true, message: '请输入密码' }]"
        >
          <a-input-password
            v-model:value="formState.password"
            placeholder="请输入密码"
            size="large"
          />
        </a-form-item>
        <a-form-item>
          <a-button type="primary" html-type="submit" size="large" block :loading="loading">
            登录
          </a-button>
        </a-form-item>
        <div class="login-footer">
          <span>还没有账号？</span>
          <router-link to="/register">立即注册</router-link>
        </div>
        <a-divider>或</a-divider>
        <div class="demo-accounts">
          <p class="demo-title">测试账号：</p>
          <p>红娘：matchmaker1 / mm123</p>
          <p>会员：13800000001 / user123</p>
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
  password: ''
})

async function handleLogin() {
  loading.value = true
  try {
    await userStore.login(formState.phone, formState.password)
    message.success('登录成功')
    if (userStore.isMatchmaker) {
      router.push('/matchmaker/dashboard')
    } else {
      router.push('/')
    }
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 420px;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-header h1 {
  font-size: 28px;
  color: #333;
  margin-bottom: 8px;
}

.login-header p {
  color: #999;
  font-size: 14px;
}

.login-footer {
  text-align: center;
  font-size: 14px;
  color: #666;
}

.login-footer a {
  color: #ff6b6b;
  text-decoration: none;
  margin-left: 4px;
}

.demo-accounts {
  text-align: center;
  font-size: 12px;
  color: #999;
}

.demo-title {
  margin-bottom: 8px;
  color: #666;
}

.demo-accounts p {
  margin: 4px 0;
}
</style>

<template>
  <a-layout class="main-layout">
    <a-layout-header class="layout-header">
      <div class="header-content">
        <div class="logo">
          <span>💕 相亲平台</span>
        </div>
        <a-menu
          theme="dark"
          mode="horizontal"
          :selected-keys="[$route.path]"
          class="header-menu"
        >
          <a-menu-item key="/recommend">
            <router-link to="/recommend">推荐</router-link>
          </a-menu-item>
          <a-menu-item key="/matches">
            <router-link to="/matches">配对</router-link>
          </a-menu-item>
          <a-menu-item key="/activities">
            <router-link to="/activities">活动</router-link>
          </a-menu-item>
          <a-menu-item key="/profile">
            <router-link to="/profile">我的</router-link>
          </a-menu-item>
        </a-menu>
        <div class="user-info">
          <a-dropdown>
            <a class="user-name">
              {{ userStore.user?.phone }}
              <a-icon type="down" />
            </a>
            <template #overlay>
              <a-menu>
                <a-menu-item @click="handleLogout">退出登录</a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>
        </div>
      </div>
    </a-layout-header>
    <a-layout-content class="layout-content">
      <router-view />
    </a-layout-content>
  </a-layout>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

function handleLogout() {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.main-layout {
  min-height: 100vh;
}

.layout-header {
  padding: 0;
  background: linear-gradient(90deg, #ff6b6b, #ee5a52);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  padding: 0 24px;
}

.logo {
  color: white;
  font-size: 20px;
  font-weight: bold;
  margin-right: 48px;
}

.header-menu {
  flex: 1;
  background: transparent;
  border-bottom: none;
}

.header-menu :deep(.ant-menu-item) {
  color: rgba(255, 255, 255, 0.85);
}

.header-menu :deep(.ant-menu-item:hover) {
  color: white;
}

.header-menu :deep(.ant-menu-item-selected) {
  color: white;
  border-bottom: 2px solid white;
}

.header-menu :deep(a) {
  color: inherit;
  text-decoration: none;
}

.user-info {
  color: white;
}

.user-name {
  color: white;
  cursor: pointer;
}

.layout-content {
  background: #f5f5f5;
}
</style>

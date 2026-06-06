<template>
  <a-layout class="matchmaker-layout">
    <a-layout-sider width="220" theme="dark">
      <div class="logo">
        <span>💕 红娘后台</span>
      </div>
      <a-menu
        theme="dark"
        mode="inline"
        :selected-keys="[$route.path]"
      >
        <a-menu-item key="/matchmaker/dashboard">
          <router-link to="/matchmaker/dashboard">数据看板</router-link>
        </a-menu-item>
        <a-menu-item key="/matchmaker/profile-review">
          <router-link to="/matchmaker/profile-review">资料审核</router-link>
        </a-menu-item>
        <a-menu-item key="/matchmaker/activities">
          <router-link to="/matchmaker/activities">活动管理</router-link>
        </a-menu-item>
        <a-menu-item key="/matchmaker/manual-match">
          <router-link to="/matchmaker/manual-match">手动牵线</router-link>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout>
      <a-layout-header class="layout-header">
        <div class="header-right">
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
      </a-layout-header>
      <a-layout-content class="layout-content">
        <router-view />
      </a-layout-content>
    </a-layout>
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
.matchmaker-layout {
  min-height: 100vh;
}

.logo {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 18px;
  font-weight: bold;
  background: rgba(255, 255, 255, 0.1);
}

.layout-header {
  background: white;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.header-right {
  display: flex;
  align-items: center;
}

.user-name {
  cursor: pointer;
  color: #333;
}

.layout-content {
  padding: 24px;
  background: #f0f2f5;
  overflow-y: auto;
}

:deep(.ant-menu-item a) {
  color: inherit;
  text-decoration: none;
}
</style>

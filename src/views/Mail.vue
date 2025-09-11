<template>
  <el-card class="function-card" shadow="hover">
    <h2>发送邮件</h2>
    <el-form :model="form" label-width="120px">
      <!-- 邮件标题 -->
      <el-form-item label="邮件标题">
        <el-input v-model="form.header" placeholder="请输入邮件标题"></el-input>
      </el-form-item>

      <!-- 邮件内容 -->
      <el-form-item label="邮件内容">
        <el-input
          type="textarea"
          v-model="form.body"
          placeholder="请输入邮件内容"
          :rows="4"
        ></el-input>
      </el-form-item>

      <!-- 接收者列表 -->
      <el-form-item label="接收者列表">
        <div class="attachment-list">
          <div v-for="(user, idx) in form.usernames" :key="idx" class="attachment-card">
            <el-input
              v-model="form.usernames[idx]"
              placeholder="请输入接收者邮箱或用户名"
              size="small"
            ></el-input>
            <el-button
              type="danger"
              size="small"
              circle
              class="delete-btn"
              @click="removeUser(idx)"
            >
              <el-icon><Delete /></el-icon>
            </el-button>
          </div>
          <el-button type="primary" size="small" class="add-btn" @click="addUser">
            <el-icon><Plus /></el-icon> 添加接收者
          </el-button>
        </div>
      </el-form-item>

      <!-- 提交按钮 -->
      <el-form-item>
        <el-button class="submit-btn" type="primary" @click="handleSubmit" :loading="isSubmitting">
          {{ isSubmitting ? '提交中...' : '发送邮件' }}
        </el-button>
      </el-form-item>
    </el-form>

    <!-- 响应卡片 -->
    <div v-if="response" class="respond-card">
      <div class="respond-card-container">
        <div class="header">
          <img class="header-image" :src="banner" alt="操作结果" />
        </div>
        <div class="body">
          <div class="message-box">
            <p class="message-text">操作结果：</p>
            <p class="code">{{ response }}</p>
          </div>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script>
import axios from 'axios'
import { Delete, Plus } from '@element-plus/icons-vue'
import banner from '@/assets/images/bg1.ccb168ef.jpg'

export default {
  name: 'MailSenderGo',
  data() {
    return {
      form: {
        header: '',
        body: '',
        usernames: [''],
      },
      isSubmitting: false,
      response: '',
      banner,
    }
  },
  methods: {
    addUser() {
      this.form.usernames.push('')
    },
    removeUser(idx) {
      this.form.usernames.splice(idx, 1)
    },
    async handleSubmit() {
      // 简单校验
      if (!this.form.header || !this.form.body) {
        this.$message.error('标题和内容不能为空')
        return
      }
      if (this.form.usernames.some((u) => !u)) {
        this.$message.error('存在空的接收者，请检查')
        return
      }

      this.isSubmitting = true
      try {
        const params = {
          cmd: 'mail', 
          header: this.form.header,
          body: this.form.body,
          usernames: this.form.usernames.join(';'),
        }
        const baseURL = localStorage.getItem('serverAddress')
        const authKey = localStorage.getItem('serverAuthKey')
        let config = { params }
        if (authKey) config.headers = { Authorization: authKey }
        const res = await axios.get(`${baseURL}/cdq/api`, config)
        if (res.data.code === 0) {
          this.$message.success('发送成功')
        } else {
          this.$message.error('操作失败' + (res.data.message ? `: ${res.data.message}` : ''))
        }
        this.response = res.data.message
      } catch (err) {
        const msg = err.response?.data?.message || err.message
        this.$message.error(msg)
        this.response = msg
      } finally {
        this.isSubmitting = false
      }
    },
  },
  components: { Delete, Plus },
}
</script>

<style scoped>
.function-card {
  max-width: 780px;
  margin: 40px auto;
  animation: fadeIn 0.6s cubic-bezier(0.23, 1, 0.32, 1);
  background: rgba(255, 255, 255, 0.96) !important;
  backdrop-filter: blur(24px) saturate(140%);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 16px;
  box-shadow:
    0 12px 40px -12px rgba(0, 0, 0, 0.12),
    0 4px 24px -4px rgba(0, 0, 0, 0.08),
    inset 0 0 12px rgba(255, 255, 255, 0.4);
  transition: all 0.3s ease;
}
.function-card:hover {
  transform: translateY(-2px);
  box-shadow:
    0 16px 48px -12px rgba(0, 0, 0, 0.16),
    0 6px 32px -4px rgba(0, 0, 0, 0.12),
    inset 0 0 16px rgba(255, 255, 255, 0.5);
}
:deep(h2) {
  color: #2c3e50 !important;
  font-weight: 600;
  margin-bottom: 24px;
  padding-bottom: 12px;
  position: relative;
}
:deep(h2::after) {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 48px;
  height: 3px;
  background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
  border-radius: 2px;
}
:deep(.el-form-item__label) {
  color: #4a5568 !important;
  font-weight: 500 !important;
  letter-spacing: 0.5px;
}
:deep(.el-input__inner),
:deep(.el-textarea__inner) {
  transition: all 0.3s ease;
  border-radius: 8px !important;
}
:deep(.el-input__inner:focus),
:deep(.el-textarea__inner:focus) {
  border-color: #4facfe !important;
  box-shadow: 0 0 0 2px rgba(79, 172, 254, 0.2) !important;
}
.submit-btn {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
  border: none !important;
  padding: 12px 32px !important;
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}
.submit-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px -4px rgba(79, 172, 254, 0.4) !important;
}
.attachment-list {
  width: 100%;
}
.attachment-card {
  margin-bottom: 12px;
  padding: 16px;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 12px;
  align-items: center;
}
.attachment-card:hover {
  transform: translateX(2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}
.delete-btn {
  padding: 8px;
  background: rgba(239, 68, 68, 0.1);
  border-color: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}
.delete-btn:hover {
  background: rgba(239, 68, 68, 0.2);
}
.add-btn {
  width: 100%;
  margin-top: 12px;
  background: rgba(59, 130, 246, 0.05);
  border: 1px dashed #3b82f6;
  color: #3b82f6;
}
.respond-card {
  display: flex;
  align-items: center;
  padding: 8px;
  color: #666;
  font-size: 14px;
  margin-top: 24px;
}
.respond-card-container {
  width: 500px;
  margin: 0 auto;
  border: 1px solid #ee9ea8;
  box-shadow: 0 0 20px #ccc;
  border-radius: 5px;
  background: #fff;
}
.header-image {
  width: 100%;
  border-radius: 5px 5px 0 0;
}
.body {
  padding: 30px 20px;
}
.message-box {
  text-align: center;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  margin: 20px auto;
}
.message-text {
  font-size: 16px;
  color: #333;
  margin: 10px 0;
}
.code {
  font-size: 18px;
  font-weight: bold;
  color: #ee9ea8;
  background: white;
  padding: 10px 20px;
  border-radius: 5px;
  display: inline-block;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.15);
}
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(16px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
@media (max-width: 768px) {
  .function-card {
    margin: 20px;
    border-radius: 12px;
  }
  :deep(h2) {
    font-size: 1.5rem;
  }
}
</style>

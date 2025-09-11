<template>
  <el-card class="function-card" shadow="hover">
    <h2>获取老师信息</h2>
    <el-form :model="form" label-width="100px">
      <el-form-item label="操作类型">
        <el-select v-model="form.type" placeholder="请选择操作类型">
          <el-option label="获取老师信息" value="getPlayer" />
          <el-option label="获取老师基础数据" value="getPlayerBasis" />
          <el-option label="登录" value="login" />
        </el-select>
      </el-form-item>

      <el-form-item label="老师SDK ID">
        <el-input v-model="form.id" placeholder="请输入老师的SDK ID">
          <template #prefix>
            <el-icon><User /></el-icon>
          </template>
        </el-input>
      </el-form-item>

      <el-form-item label="老师游戏ID">
        <el-input v-model="form.accountServerId" placeholder="请输入老师的游戏ID (UID)">
          <template #prefix>
            <el-icon><User /></el-icon>
          </template>
        </el-input>
      </el-form-item>
      <el-form-item>
        <el-button class="gradient-button" type="primary" @click="handleGetTeacher">提交</el-button>
      </el-form-item>
    </el-form>
    <!-- 响应卡片 -->
    <div v-if="response" class="respond-card">
      <div class="respond-card-container">
        <div class="header">
          <img class="header-image" :src="banner1" alt="操作结果" />
        </div>
        <div class="body">
          <div class="message-box">
            <p class="message-text">老师！这是您的操作结果：</p>
            <div class="code-container">
              <el-button 
                class="copy-button" 
                size="small" 
                type="primary" 
                @click="copyToClipboard"
                :icon="copyIcon"
              >
                复制
              </el-button>
              <p class="code">{{ response }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script>
import axios from 'axios'
import { User, DocumentCopy } from '@element-plus/icons-vue'
import banner1 from '@/assets/images/bg1.ccb168ef.jpg'

export default {
  name: 'Player',
  components: { User, DocumentCopy },
  data() {
    return {
      form: {
        type: '',
        id: '',
        accountServerId: '',
      },
      response: '',
      responseType: '',
      banner1: banner1,
      copyIcon: DocumentCopy,
    }
  },
  methods: {
    async handleGetTeacher() {
      const baseURL = localStorage.getItem('serverAddress')
      const authKey = localStorage.getItem('serverAuthKey')

      if (!baseURL) {
        this.$message.error('请先在首页保存服务器地址')
        return
      }

      if (!this.form.type) {
        this.$message.error('请选择操作类型')
        return
      }

      try {
        const paramsObj = {
          cmd: 'player',
          type: this.form.type,
        }

        if (this.form.id) {
          paramsObj.id = this.form.id
        }

        if (this.form.accountServerId) {
          paramsObj.accountServerId = this.form.accountServerId
        }

        const params = new URLSearchParams(paramsObj).toString()

        const res = await axios.get(`${baseURL}/cdq/api?${params}`, {
          headers: authKey ? { Authorization: authKey } : {},
        })

        if (res.data.code === 0) {
          this.responseType = 'success'
          this.$message.success('操作成功')
          
          let displayData = res.data.data
          if (typeof displayData === 'string') {
            try {
              displayData = JSON.parse(displayData)
            } catch (parseError) {
              console.warn('JSON解析失败:', parseError)
            }
          }
          this.response = JSON.stringify(displayData, null, 2)
        } else {
          this.responseType = 'error'
          this.$message.error('操作失败：' + (res.data.message || '请查看响应获取具体错误'))
          this.response = res.data.message || '未知错误'
        }
      } catch (error) {
        this.responseType = 'error'
        const errorMsg = error.response?.data?.message || error.message
        this.response = errorMsg
        this.$message.error(this.response)
      }
    },

    async copyToClipboard() {
      try {
        await navigator.clipboard.writeText(this.response)
        this.$message.success('已复制到剪贴板')
      } catch (err) {
        // 降级处理：使用传统方法
        try {
          const textArea = document.createElement('textarea')
          textArea.value = this.response
          document.body.appendChild(textArea)
          textArea.select()
          document.execCommand('copy')
          document.body.removeChild(textArea)
          this.$message.success('已复制到剪贴板')
        } catch (fallbackErr) {
          this.$message.error('复制失败，请手动选择复制')
        }
      }
    },
  },
}
</script>

<style scoped>
.function-card {
  max-width: 780px;
  margin: 20px auto;
  animation: fadeIn 0.6s cubic-bezier(0.23, 1, 0.32, 1);
  background: rgba(255, 255, 255, 0.96);
  backdrop-filter: blur(24px) saturate(140%);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 16px;
  box-shadow: 0 12px 40px -12px rgba(0, 0, 0, 0.12);
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
  margin: 0 24px 24px;
  padding-bottom: 12px;
  border-bottom: 1px solid #e2e8f0;
  position: relative;
}

:deep(h2::after) {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
  border-radius: 2px;
}

.respond-card {
  display: flex;
  align-items: center;
  padding: 8px;
  color: #666;
  font-size: 14px;
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
  max-width: 450px;
  margin: 20px auto;
}

.message-text {
  font-size: 16px;
  color: #333;
  margin: 10px 0;
}

.code-container {
  position: relative;
}

.code {
  font-size: 14px;
  font-weight: bold;
  color: #ee9ea8;
  background: white;
  padding: 10px 20px;
  border-radius: 5px;
  display: block;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.15);
  word-wrap: break-word;
  word-break: break-all;
  white-space: pre-wrap;
  max-width: 100%;
  text-align: left;
  font-family: 'Courier New', monospace;
  margin-top: 10px;
}

.copy-button {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
  border: none !important;
  padding: 6px 12px !important;
  font-size: 12px !important;
  transition: transform 0.2s ease;
}

.copy-button:hover {
  transform: translateY(-1px);
}

.gradient-button {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
  border: none !important;
  padding: 12px 32px !important;
  transition: transform 0.2s ease;
}

.gradient-button:hover {
  transform: translateY(-2px);
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
</style>

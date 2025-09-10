<template>
  <el-card class="function-card" shadow="hover">
    <h2>命令生成器</h2>
    <el-form :model="form" :rules="rules" ref="commandForm" label-width="120px">
      <!-- API地址设置 -->
      <el-form-item label="API地址" prop="apiPath">
        <el-input v-model="form.apiPath" placeholder="请输入API路径">
          <template #prefix>
            <el-icon><Link /></el-icon>
          </template>
        </el-input>
      </el-form-item>

      <!-- 参数列表 -->
      <el-form-item label="请求参数">
        <div class="parameter-list">
          <div v-for="(param, index) in form.parameters" :key="index" class="parameter-card">
            <div class="parameter-content">
              <!-- 参数键 -->
              <div class="field-group">
                <div class="field-label">
                  参数键
                  <el-tooltip content="输入参数名称，如 cmd、uid 等" placement="top">
                    <el-icon class="tip-icon"><QuestionFilled /></el-icon>
                  </el-tooltip>
                </div>
                <el-input
                  v-model="param.key"
                  placeholder="如: cmd"
                  size="small"
                  class="param-input"
                />
              </div>
              <!-- 参数值 -->
              <div class="field-group">
                <div class="field-label">
                  参数值
                  <el-tooltip content="输入参数值" placement="top">
                    <el-icon class="tip-icon"><QuestionFilled /></el-icon>
                  </el-tooltip>
                </div>
                <el-input
                  v-model="param.value"
                  size="small"
                  class="param-input"
                />
              </div>
              <!-- 删除按钮 -->
              <el-button
                type="danger"
                size="small"
                circle
                class="delete-btn"
                @click="removeParameter(index)"
              >
                <el-icon><Delete /></el-icon>
              </el-button>
            </div>
          </div>
          <el-button type="primary" size="small" class="add-btn" @click="addParameter">
            <el-icon><Plus /></el-icon> 添加参数
          </el-button>
        </div>
      </el-form-item>

      <!-- 提交按钮 -->
      <el-form-item>
        <el-button class="submit-btn" type="primary" @click="handleSubmit" :loading="isSubmitting">
          {{ isSubmitting ? '请求中...' : '发送请求' }}
        </el-button>
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
            <p class="message-text2">老师！这是您的操作结果：</p>
            <p class="message-text">请求URL：</p>
            <p class="url-text">{{ requestUrl }}</p>
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
import { Link, Delete, Plus, QuestionFilled } from '@element-plus/icons-vue'
import banner1 from '@/assets/images/bg1.ccb168ef.jpg'

export default {
  name: 'CommandSender',
  data() {
    return {
      form: {
        apiPath: '/cdq/api',
        parameters: [
          { key: 'cmd', value: 'help' },
        ],
      },
      isSubmitting: false,
      response: '',
      requestUrl: '',
      banner1,
      rules: {
        apiPath: [{ required: true, message: '请输入API路径', trigger: 'blur' }],
      },
    }
  },
  methods: {
    addParameter() {
      this.form.parameters.push({ key: '', value: '' })
    },
    removeParameter(index) {
      this.form.parameters.splice(index, 1)
    },
    async handleSubmit() {
      this.$refs.commandForm.validate(async (valid) => {
        if (!valid) return
        this.isSubmitting = true

        const baseURL = localStorage.getItem('serverAddress')
        const authKey = localStorage.getItem('serverAuthKey')

        // 构建参数对象
        const params = {}
        this.form.parameters.forEach(param => {
          if (param.key && param.value) {
            params[param.key] = param.value
          }
        })

        // 构建完整URL用于显示
        const urlParams = new URLSearchParams(params)
        this.requestUrl = `${baseURL}${this.form.apiPath}?${urlParams.toString()}`

        try {
          const config = { params }
          if (authKey) {
            config.headers = { Authorization: authKey }
          }
          
          const res = await axios.get(`${baseURL}${this.form.apiPath}`, config)
          
          if (res.data.code === 0) {
            this.$message.success('请求成功，请老师查收~')
          } else {
            this.$message.warning('请求完成，但返回了错误码')
          }
          
          // 格式化响应数据
          this.response = typeof res.data === 'object' 
            ? JSON.stringify(res.data, null, 2) 
            : res.data
            
        } catch (err) {
          const msg = err.response?.data?.message || err.message
          this.$message.error(`请求失败: ${msg}`)
          this.response = `错误: ${msg}`
        } finally {
          this.isSubmitting = false
        }
      })
    },
  },
  components: {
    Link,
    Delete,
    Plus,
    QuestionFilled,
  },
}
</script>

<style scoped>
.parameter-list {
  width: 100%;
}

.parameter-card {
  margin-bottom: 12px;
  padding: 16px;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
}

.parameter-card:hover {
  transform: translateX(2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.parameter-content {
  display: grid;
  grid-template-columns: 1fr 1fr 40px;
  gap: 12px;
  align-items: center;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.field-label {
  font-size: 12px;
  color: #64748b;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 4px;
}

.tip-icon {
  font-size: 14px;
  color: #94a3b8;
}

.param-input {
  width: 100%;
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

/* 响应卡片样式 */
.respond-card {
  display: flex;
  align-items: center;
  padding: 8px;
  color: #666;
  font-size: 14px;
  margin-top: 24px;
}

.respond-card-container {
  width: 100%;
  max-width: 600px;
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
  text-align: left;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  margin: 20px auto;
}

.message-text {
  font-size: 16px;
  color: #333;
  margin: 10px 0 5px 0;
  font-weight: 600;
}

.message-text2 {
  font-size: 16px;
  color: #333;
  margin: 10px 0;
  text-align: center;
}

.url-text {
  font-size: 14px;
  color: #666;
  background: #f8fafc;
  padding: 8px 12px;
  border-radius: 4px;
  border: 1px solid #e2e8f0;
  word-break: break-all;
  margin-bottom: 15px;
  font-family: monospace;
}

/* .code {
  font-size: 14px;
  color: #333;
  background: #f8fafc;
  padding: 15px;
  border-radius: 5px;
  border: 1px solid #e2e8f0;
  white-space: pre-wrap;
  font-family: monospace;
  max-height: 300px;
  overflow-y: auto;
} */

.code {
  font-size: 14px;
  font-weight: bold;
  color: #ee9ea8;
  background: white;
  padding: 10px 20px;
  border-radius: 5px;
  display: inline-block;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.15);
  word-wrap: break-word;
  word-break: break-all;
  white-space: pre-wrap;
  max-width: 100%;
}


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

:deep(.el-input__prefix) {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  padding: 0 !important;
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

  .parameter-content {
    grid-template-columns: 1fr;
    gap: 8px;
  }
}
</style>

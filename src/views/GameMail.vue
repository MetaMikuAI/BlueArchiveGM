<template>
  <el-card class="function-card" shadow="hover">
    <h2>发送邮件</h2>
    <el-form :model="form" :rules="rules" ref="mailForm" label-width="120px">
      <!-- 邮件选项 -->
      <el-form-item label="邮件选项" prop="player_type">
        <el-radio-group v-model="form.player_type">
          <el-radio :label="0">全局</el-radio>
          <el-radio :label="1">私人</el-radio>
        </el-radio-group>
      </el-form-item>

      <!-- UID输入 -->
      <el-form-item v-if="form.player_type === 1" label="UID" prop="uid">
        <el-input v-model="form.uid" placeholder="请输入玩家UID">
          <template #prefix>
            <el-icon><User /></el-icon>
          </template>
        </el-input>
      </el-form-item>

      <!-- 发件人 -->
      <el-form-item label="发件人" prop="sender">
        <el-input v-model="form.sender" placeholder="请输入发件人名称">
          <template #prefix>
            <el-icon><Message /></el-icon>
          </template>
        </el-input>
      </el-form-item>

      <!-- 邮件内容 -->
      <el-form-item label="邮件内容" prop="comment">
        <el-input
          type="textarea"
          v-model="form.comment"
          placeholder="请输入邮件内容"
          :rows="4"
        ></el-input>
      </el-form-item>

      <!-- 时间设置 -->
      <el-form-item label="发送时间" prop="send_time">
        <el-date-picker
          v-model="form.send_time"
          type="datetime"
          value-format="X"
          placeholder="选择发送时间"
          style="width: 100%"
        ></el-date-picker>
      </el-form-item>
      <el-form-item label="过期时间" prop="expire_time">
        <el-date-picker
          v-model="form.expire_time"
          type="datetime"
          value-format="X"
          placeholder="选择过期时间"
          style="width: 100%"
        ></el-date-picker>
      </el-form-item>

      <!-- 附件列表 -->
      <el-form-item label="附件列表">
        <div class="attachment-list">
          <div v-for="(item, index) in form.parcel_info_list" :key="index" class="attachment-card">
            <div class="attachment-content">
              <!-- 附件类型 -->
              <div class="field-group">
                <div class="field-label">
                  附件类型
                  <el-tooltip content="选择附件类型（0表示无类型附件）" placement="top">
                    <el-icon class="tip-icon"><QuestionFilled /></el-icon>
                  </el-tooltip>
                </div>
                <el-select v-model="item.type" placeholder="必填" size="small" class="type-select">
                  <el-option
                    v-for="option in typeOptions"
                    :key="option.value"
                    :label="option.label"
                    :value="option.value"
                  />
                </el-select>
              </div>
              <!-- 物品ID -->
              <div class="field-group">
                <div class="field-label">
                  物品ID
                  <el-tooltip content="输入游戏内物品ID，最多7位数" placement="top">
                    <el-icon class="tip-icon"><QuestionFilled /></el-icon>
                  </el-tooltip>
                </div>
                <el-input-number
                  v-model.number="item.id"
                  :min="0"
                  :max="999999"
                  class="id-input"
                  size="small"
                />
              </div>
              <!-- 数量 -->
              <div class="field-group">
                <div class="field-label">
                  数量
                  <el-tooltip content="必须大于等于0的整数，最大999" placement="top">
                    <el-icon class="tip-icon"><QuestionFilled /></el-icon>
                  </el-tooltip>
                </div>
                <el-input-number
                  v-model.number="item.num"
                  :min="0"
                  :max="999"
                  class="num-input"
                  size="small"
                />
              </div>
              <!-- 删除按钮 -->
              <el-button
                type="danger"
                size="small"
                circle
                class="delete-btn"
                @click="removeAttachment(index)"
              >
                <el-icon><Delete /></el-icon>
              </el-button>
            </div>
          </div>
          <el-button type="primary" size="small" class="add-btn" @click="addAttachment">
            <el-icon><Plus /></el-icon> 添加附件
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
          <img class="header-image" :src="banner1" alt="操作结果" />
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
import { User, Message, Delete, Plus, QuestionFilled } from '@element-plus/icons-vue'
import banner1 from '@/assets/images/bg1.ccb168ef.jpg'

export default {
  name: 'MailSender',
  data() {
    return {
      form: {
        player_type: 0,
        uid: '',
        sender: 'BaPsServer',
        comment: '请查收邮件',
        send_time: null,
        expire_time: null,
        parcel_info_list: [],
      },
      typeOptions: [
        { value: 1, label: '学生' },
        { value: 2, label: '货币' },
        { value: 3, label: '装备' },
        { value: 4, label: '物品' },
        { value: 5, label: '卡池' },
        { value: 6, label: '商品' },
        { value: 7, label: '商店' },
        { value: 8, label: '记忆大厅' },
        { value: 9, label: '账号经验' },
        { value: 10, label: '学生经验' },
        { value: 11, label: '好感经验' },
        { value: 12, label: 'TSS' },
        { value: 13, label: '家具' },
        { value: 14, label: '商店刷新' },
        { value: 15, label: '地点经验' },
        { value: 16, label: '配方' },
        { value: 17, label: '学生武器' },
        { value: 18, label: '月度商品' },
        { value: 19, label: '学生装备' },
        { value: 20, label: '资料背景' },
        { value: 21, label: '徽章' },
        { value: 22, label: '贴纸' },
        { value: 23, label: '服饰' },
      ],
      isSubmitting: false,
      response: '',
      banner1,
      rules: {
        sender: [{ required: true, message: '请输入发件人', trigger: 'blur' }],
        comment: [{ required: true, message: '请输入邮件内容', trigger: 'blur' }],
        send_time: [
          { type: 'datetime', required: true, message: '请选择发送时间', trigger: 'change' },
        ],
        expire_time: [
          { type: 'datetime', required: true, message: '请选择过期时间', trigger: 'change' },
        ],
        uid: [
          {
            required: true,
            message: '私人邮件必须填写UID',
            trigger: 'blur',
            validator: (rule, value) => {
              if (this.form.player_type === 1 && !value) return new Error('UID不能为空')
              return true
            },
          },
        ],
      },
    }
  },
  methods: {
    addAttachment() {
      this.form.parcel_info_list.push({ type: 0, id: 0, num: 0 })
    },
    removeAttachment(index) {
      this.form.parcel_info_list.splice(index, 1)
    },
    async handleSubmit() {
      this.$refs.mailForm.validate(async (valid) => {
        if (!valid) return
        this.isSubmitting = true

        const baseURL = localStorage.getItem('serverAddress')
        const authKey = localStorage.getItem('serverAuthKey')

        const params = {
          cmd: 'gameMail',
          recipient: this.form.player_type === 0 ? 'all' : this.form.uid,
          sender: this.form.sender || 'gucooing',
          comment: this.form.comment || '请查收邮件',
          sendTime: this.form.send_time || 946656000,
          expireTime: this.form.expire_time || 4070880000,
          parcelInfoList: JSON.stringify(
            this.form.parcel_info_list.map((item) => ({
              type: item.type,
              id: item.id,
              num: item.num,
            })),
          ),
        }

        try {
          const config = { params }
          if (authKey) config.headers = { Authorization: authKey }
          const res = await axios.get(`${baseURL}/cdq/api`, config)
          if (res.data.code === 0) {
            this.$message.success('发送成功')
          } else {
            this.$message.error('发送失败')
          }
          this.response = res.data.message
        } catch (err) {
          const msg = err.response?.data?.message || err.message
          this.$message.error(msg)
          this.response = msg
        } finally {
          this.isSubmitting = false
        }
      })
    },
  },
  components: {
    User,
    Message,
    Delete,
    Plus,
    QuestionFilled,
  },
}
</script>

<style scoped>
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
}

.attachment-card:hover {
  transform: translateX(2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.attachment-content {
  display: grid;
  grid-template-columns: 160px 1fr 1fr 40px;
  gap: 12px;
  align-items: center;
}

.type-select {
  width: 100%;
}

.id-input,
.num-input {
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

/* 新增响应卡片样式 */
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

/* 以下为原有美化部分 */
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
}
</style>

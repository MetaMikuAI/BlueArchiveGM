<template>
  <el-card class="function-card" shadow="hover">
    <h2>游戏设置</h2>
    <el-form :model="form" label-width="120px">
      <!-- 玩家UID -->
      <el-form-item label="玩家UID">
        <el-input v-model="form.uid" placeholder="请输入玩家UID" type="number"></el-input>
      </el-form-item>

      <!-- 类型选择 -->
      <el-form-item label="类型">
        <el-select v-model="form.type" placeholder="请选择类型" @change="handleTypeChange">
          <el-option label="设置玩家等级" value="AccountLevel"></el-option>
          <el-option label="设置玩家通知" value="Toast"></el-option>
          <el-option label="获取服务器配置" value="GetConfig"></el-option>
          <el-option label="一键通关走格子" value="Campaign"></el-option>
          <el-option label="接收邮件" value="ReceiveMail"></el-option>
        </el-select>
      </el-form-item>

      <!-- sub1 输入框 -->
      <el-form-item v-if="showSub1" :label="sub1Label">
        <el-input
          v-model="form.sub1"
          :placeholder="sub1Placeholder"
          :type="form.type === 'AccountLevel' ? 'number' : 'text'"
          :disabled="!form.type"
        ></el-input>
      </el-form-item>

      <!-- 提交按钮 -->
      <el-form-item>
        <el-button class="submit-btn" type="primary" @click="handleSetGame" :loading="isSubmitting">
          {{ isSubmitting ? '提交中...' : '提交' }}
        </el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script>
import axios from 'axios'
import banner1 from '@/assets/images/bg1.ccb168ef.jpg'

export default {
  name: 'SetGame',
  data() {
    return {
      form: {
        uid: '',
        type: '',
        sub1: '',
      },
      response: '',
      isSubmitting: false,
    }
  },
  computed: {
    // sub1 的标签，根据 type 区分
    sub1Label() {
      switch (this.form.type) {
        case 'AccountLevel':
          return '等级'
        case 'Toast':
          return '通知'
        case 'GetConfig':
        case 'Campaign':
          return '占位参数'
        default:
          return '参数'
      }
    },
    // sub1 的占位符
    sub1Placeholder() {
      switch (this.form.type) {
        case 'AccountLevel':
          return '请输入玩家等级（数字）'
        case 'Toast':
          return '请输入通知内容'
        case 'GetConfig':
        case 'Campaign':
          return '请输入任意值'
        default:
          return '请选择类型'
      }
    },
    showSub1() {
      return ['AccountLevel', 'Toast'].includes(this.form.type)
    },
    banner1() {
      return banner1
    },
  },
  methods: {
    handleTypeChange() {
      this.form.sub1 = ''
    },
    async handleSetGame() {
      const baseURL = localStorage.getItem('serverAddress')
      const authKey = localStorage.getItem('serverAuthKey')
      if (!baseURL) {
        this.$message.error('请先在首页保存服务器地址')
        return
      }
      const needsSub1 = ['AccountLevel', 'Toast'].includes(this.form.type)
      if (!this.form.uid || !this.form.type || (needsSub1 && !this.form.sub1)) {
        this.$message.error('请填写完整信息')
        return
      }
      this.isSubmitting = true
      try {
        let url = `${baseURL}/cdq/api?cmd=set&uid=${this.form.uid}&type=${this.form.type}&sub1=${encodeURIComponent(this.form.sub1)}`
        const headers = {}
        if (authKey) headers.Authorization = authKey
        const res = await axios.get(url, { headers })
        if (res.data.code === 0) {
          this.$message.success('操作成功')
        } else {
          this.$message.error('操作失败' + (res.data.message ? `: ${res.data.message}` : ''))
        }
      } catch (error) {
        this.$message.error(error.response?.data?.message || error.message)
      } finally {
        this.isSubmitting = false
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
  box-shadow: 0 16px 48px -12px rgba(0, 0, 0, 0.16);
}

.submit-btn {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
  border: none !important;
  padding: 12px 32px !important;
}

.submit-btn:hover {
  transform: translateY(-1px);
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
</style>

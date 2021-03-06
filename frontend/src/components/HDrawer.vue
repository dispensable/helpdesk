<template>
  <div>
    <a-drawer
      key="h-drawer"
      title="Admin Panel"
      :width="720"
      placement="right"
      :closable="false"
      @close="onClose"
      :visible="visible"
    >
      <div slot="handle" class="ant-pro-setting-drawer-handle" @click="showDrawer">
        <a-icon type="setting" :style="{color: '#fff', fontSize: '20px'}"/>
      </div>

      <a-form v-for="(paramRule, index) in paramRules"
              :key="index"
              method="POST"
              layout="vertical"
              hideRequiredMark
              @submit="(e) => onSubmit(e, index)"
      >
        <a-row :gutter="16">
          <a-col>
            <a-form-item label="Title">
              <a-input name="title" placeholder="Untitled"
                       v-model="paramRule.title"
              ></a-input>
            </a-form-item>
          </a-col>
        </a-row>
        <a-row :gutter="16">
          <a-col>
            <a-form-item label="Rule">
              <a-textarea name="rule"
                          rows="1"
                          placeholder='e.g. ["onlycontains", ["split", "hosts", ","], "host1", "host2", "host3"]'
                          autosize
                          required="true"
                          v-model="paramRule.rule"
              ></a-textarea>
            </a-form-item>
          </a-col>
        </a-row>
        <a-row :gutter="16">
          <a-col :span="6">
            <a-form-item label="Is auto-approval?">
              <a-checkbox name="is_auto_approval"
                          :checked="paramRule.is_auto_approval"
                          @change="(e) => onCheckboxChange(e, index, 'is_auto_approval')"
              ></a-checkbox>
            </a-form-item>
          </a-col>
          <a-col :span="18">
            <a-form-item label="Approver">
              <a-input name="approver" placeholder="Approver names seperated by comma"
                       v-model="paramRule.approver"
              ></a-input>
            </a-form-item>
          </a-col>
        </a-row>

        <a-form-item :style="{textAlign: 'right'}"
        >
          <a-button type="danger" shape="circle" icon="close"
                    :style="{marginRight: '8px'}"
                    :disabled="paramRules.length - 1 === index"
                    @click="(e) => onDelete(e, index)"
          />
          <a-button html-type="submit" type="primary" shape="circle" icon="check" />
        </a-form-item>

        <a-divider />
      </a-form>

      <div>
        <a-collapse accordion :bordered="false">
          <a-collapse-panel header="Debug Info" key="1">
            <div>
              <p>{{ actionDefinition }}</p>
            </div>
          </a-collapse-panel>
        </a-collapse>
      </div>

    </a-drawer>
  </div>
</template>

<script>
import {HRequest} from '../utils/HRequests'
export default {
  name: 'HDrawer',
  props: ['actionDefinition'],
  data () {
    return {
      visible: false,
      handle: 'handle',
      paramRules: null
    }
  },
  computed: {
    currentForm () {
      return this.$route.params.name
    },
    url_param_rule () {
      return '/api/admin_panel/' + this.currentForm + '/param_rule'
    },
    url_param_rule_add () {
      return '/api/admin_panel/' + this.currentForm + '/param_rule/add'
    },
    url_param_rule_del () {
      return '/api/admin_panel/' + this.currentForm + '/param_rule/del'
    }
  },
  watch: {
    '$route' () {
      // reload ActionDefinition when url changes
      this.clearStage()
    }
  },
  methods: {
    clearStage () {
      // clear stage , close the drawer
      this.paramRules = null
      this.onClose()
    },
    showDrawer () {
      this.loadParamRules()
      this.visible = !this.visible
    },
    loadParamRules () {
      if (this.paramRules) {
        return
      }
      this.paramRules = [{}]
      HRequest.get(this.url_param_rule).then(
        (response) => {
          if (response.status === 200 && response.data.data) {
            if (response.data.data !== []) {
              this.paramRules = response.data.data
            }
          }
          this.paramRules.push({})
        }
      )
    },
    onClose () {
      this.visible = false
    },
    onCheckboxChange (e, index, attr) {
      var paramRule = this.paramRules[index]
      paramRule[attr] = e.target.checked
      this.paramRules.splice(index, 1, paramRule)
    },
    onSubmit (e, index) {
      e.preventDefault()

      let this_ = this
      let message = this.$message

      let xhr = new XMLHttpRequest()
      xhr.responseType = 'json'
      xhr.onreadystatechange = function () {
        if (this.readyState === 4) {
          var jsonResponse = xhr.response
          if (this.status === 200) {
            var paramRuleAdded = jsonResponse.data
            message.success(JSON.stringify(paramRuleAdded))
            this_.paramRules.splice(index, 1, paramRuleAdded)
            // new empty obj if last
            if (this_.paramRules.length - 1 === index) {
              this_.paramRules.push({})
            }
          } else {
            message.warning(JSON.stringify(jsonResponse))
          }
        }
      }
      xhr.open('POST', this.url_param_rule_add, true)
      xhr.setRequestHeader('Content-type', 'application/json')
      xhr.send(JSON.stringify(this.paramRules[index]))
    },
    onDelete (e, index) {
      let this_ = this
      let message = this.$message

      let xhr = new XMLHttpRequest()
      xhr.responseType = 'json'
      xhr.onreadystatechange = function () {
        if (this.readyState === 4) {
          var jsonResponse = xhr.response
          if (this.status === 200) {
            var paramRuleAdded = jsonResponse.data
            message.success(JSON.stringify(paramRuleAdded))
            this_.paramRules.splice(index, 1)
          } else {
            message.warning(JSON.stringify(jsonResponse))
          }
        }
      }
      xhr.open('POST', this.url_param_rule_del, true)
      xhr.setRequestHeader('Content-type', 'application/json')
      xhr.send(JSON.stringify(this.paramRules[index]))
    }

  }
}
</script>

<style scoped>
.ant-pro-setting-drawer-handle {
  position: absolute;
  top: 240px;
  right: 720px;
  z-index: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  font-size: 16px;
  text-align: center;
  background: #1890ff;
  border-radius: 4px 0 0 4px;
  cursor: pointer;
  pointer-events: auto;
}
</style>

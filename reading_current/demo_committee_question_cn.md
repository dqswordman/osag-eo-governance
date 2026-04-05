# Demo V2 常见追问简答

## 1. 这是真实数据还是 synthetic 场景？
短答：这是工程化 synthetic 场景，但严格对齐 thesis 的治理逻辑。

## 2. 它和 thesis benchmark 的关系是什么？
短答：benchmark 提供正式证据，demo 提供运行行为解释。

## 3. 为什么这不是更好看的可视化而已？
短答：因为它展示了 target、actual、deadline、backlog 和 policy gap，不只是展示结果图片。

## 4. policy 是在哪里进入选择的？
短答：进入 target share、coverage gap、deadline pressure 和 backlog 这些量。

## 5. 为什么不一直追最高优先级？
短答：因为那样会让别的合同长期饥饿，长期服务会偏离政策目标。

## 6. 这里到底在监控什么？
短答：监控合同层面的目标份额、实际份额、偏差、时限压力和积压。

## 7. 为什么 OSAG 比 heuristic 更像工程系统？
短答：因为它不仅决定“现在选谁”，还持续检查“长期服务是否还合规”。

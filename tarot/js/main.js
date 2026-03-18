// 主逻辑文件 - 最终修复版

// 防止重复初始化
let isInitialized = false;

// 广告配置
const adConfig = {
    enabled: false,
    adUnitId: '',
};

// 全局变量
let currentCards = [];
let selectedCards = [];
let flippedCount = 0;

// 页面切换（添加错误处理）
function showPage(pageId) {
    try {
        document.querySelectorAll('.page').forEach(page => {
            page.classList.remove('active');
        });
        const target = document.getElementById(pageId);
        if (target) {
            target.classList.add('active');
            console.log('切换到页面:', pageId);
        } else {
            console.error('页面不存在:', pageId);
        }
    } catch (error) {
        console.error('showPage 错误:', error);
    }
    window.scrollTo(0, 0);
}

// 渲染双列 78 张牌（每列 39 张）
function renderFanCards() {
    try {
        const container = document.getElementById('fan-container');
        if (!container) {
            console.error('fan-container 不存在');
            return;
        }
        
        container.innerHTML = '';
        container.style.display = 'flex';
        container.style.justifyContent = 'center';
        container.style.gap = '20px';
        
        const totalCards = 78;
        const cardsPerColumn = 26;
        const totalColumns = 3;
        
        // 创建三列
        const columns = [];
        for (let c = 0; c < totalColumns; c++) {
            const column = document.createElement('div');
            column.className = 'card-column';
            columns.push(column);
        }
        
        for (let i = 0; i < totalCards; i++) {
            const card = document.createElement('div');
            card.className = 'fan-card';
            card.dataset.index = i;
            card.style.background = `url('images/back/back_v2.jpg?v=${Date.now()}') center/cover no-repeat`;
            card.style.backgroundColor = '#1a237e';
            
            // 点击选牌
            card.addEventListener('click', (e) => {
                e.stopPropagation();
                toggleSelectCard(i, card);
            });
            
            // 分配到三列（循环分配）
            const columnIndex = i % totalColumns;
            columns[columnIndex].appendChild(card);
        }
        
        columns.forEach(column => container.appendChild(column));
        console.log('牌面渲染完成');
    } catch (error) {
        console.error('renderFanCards 错误:', error);
    }
}

// 切换选牌
function toggleSelectCard(index, cardElement) {
    try {
        const cardIndex = selectedCards.indexOf(index);
        
        if (cardIndex > -1) {
            // 取消选择
            selectedCards.splice(cardIndex, 1);
            cardElement.classList.remove('selected');
            cardElement.style.opacity = '1';
            cardElement.style.transform = 'scale(1)';
            cardElement.style.boxShadow = '0 5px 15px rgba(0, 0, 0, 0.5)';
        } else {
            // 选择
            if (selectedCards.length >= 3) {
                alert('最多选择 3 张牌');
                return;
            }
            selectedCards.push(index);
            cardElement.classList.add('selected');
            cardElement.style.opacity = '1';
            cardElement.style.transform = 'scale(1.05)';
            cardElement.style.boxShadow = '0 0 25px rgba(255, 183, 77, 0.9)';
        }
        
        // 未选中的牌变暗
        document.querySelectorAll('.fan-card').forEach((card, idx) => {
            if (!selectedCards.includes(idx)) {
                card.style.opacity = '0.6';
                card.style.transform = 'scale(1)';
                card.style.boxShadow = '0 5px 15px rgba(0, 0, 0, 0.5)';
            }
        });
        
        // 更新计数
        const countSpan = document.getElementById('selected-count');
        if (countSpan) {
            countSpan.textContent = selectedCards.length;
        }
        
        // 启用/禁用确认按钮
        const confirmBtn = document.getElementById('confirm-select-btn');
        if (confirmBtn) {
            confirmBtn.disabled = selectedCards.length !== 3;
            confirmBtn.textContent = selectedCards.length === 3 ? '✅ 确认选牌' : `已选 ${selectedCards.length}/3 张`;
        }
    } catch (error) {
        console.error('toggleSelectCard 错误:', error);
    }
}

// 确认选牌
function handleConfirmSelect() {
    try {
        if (selectedCards.length !== 3) {
            alert('请选择 3 张牌');
            return;
        }
        
        // 从 78 张中抽取选中的 3 张
        currentCards = selectedCards.map(idx => {
            const cardData = tarotDeck[idx];
            return {
                ...cardData,
                position: Math.random() > 0.5 ? 'upright' : 'reversed',
                positionName: Math.random() > 0.5 ? '正位' : '逆位'
            };
        });
        
        console.log('抽到的牌:', currentCards);
        
        // 进入翻牌页面
        showPage('flip-page');
        
        // 重置翻牌状态
        flippedCount = 0;
        document.querySelectorAll('.card').forEach(card => {
            card.classList.remove('flipped', 'reversed');
            const front = card.querySelector('.card-front');
            if (front) front.remove();
        });
        
        // 隐藏解锁区域
        const unlockSection = document.getElementById('unlock-section');
        if (unlockSection) {
            unlockSection.style.display = 'none';
        }
    } catch (error) {
        console.error('handleConfirmSelect 错误:', error);
    }
}

// 翻牌逻辑
function flipCard(index) {
    try {
        const cardSlot = document.querySelector(`.card-slot[data-index="${index}"]`);
        if (!cardSlot) {
            console.error('card-slot 不存在:', index);
            return;
        }
        
        const card = cardSlot.querySelector('.card');
        if (!card || card.classList.contains('flipped')) {
            return;
        }
        
        card.classList.add('flipped');
        
        const cardData = currentCards[index];
        if (!cardData) {
            console.error('牌数据不存在:', index);
            return;
        }
        
        // 创建牌面
        const oldFront = card.querySelector('.card-front');
        if (oldFront) oldFront.remove();
        
        const cardFront = document.createElement('div');
        cardFront.className = 'card-front';
        const img = document.createElement('img');
        img.src = `images/${cardData.image}`;
        img.alt = cardData.name;
        img.loading = 'lazy';
        img.onerror = () => {
            console.error('图片加载失败:', cardData.image);
        };
        cardFront.appendChild(img);
        card.appendChild(cardFront);
        
        // 如果是逆位，添加反转 class
        if (cardData.position === 'reversed') {
            setTimeout(() => {
                card.classList.add('reversed');
            }, 400);
        }
        
        flippedCount++;
        
        if (flippedCount === 3) {
            setTimeout(() => {
                const unlockSection = document.getElementById('unlock-section');
                if (unlockSection) {
                    unlockSection.style.display = 'block';
                }
            }, 500);
        }
    } catch (error) {
        console.error('flipCard 错误:', error);
    }
}

// 显示解读
function showReading() {
    try {
        currentCards.forEach((card, index) => {
            const img = document.getElementById(`card-${index}-img`);
            const nameEl = document.getElementById(`card-${index}-name`);
            const readingEl = document.getElementById(`card-${index}-reading`);
            
            if (img) img.src = `images/${card.image}`;
            if (nameEl) {
                const positionText = card.position === 'upright' ? '正位' : '逆位';
                nameEl.textContent = `${card.name} ${positionText}`;
            }
            if (readingEl) {
                readingEl.innerHTML = getCardReading(card, index);
            }
        });
        
        const summary = generateSummary(currentCards);
        const summaryEl = document.getElementById('summary-reading');
        if (summaryEl) {
            summaryEl.innerHTML = summary;
        }
        
        showPage('reading-page');
        
        flippedCount = 0;
        const unlockSection = document.getElementById('unlock-section');
        if (unlockSection) {
            unlockSection.style.display = 'none';
        }
    } catch (error) {
        console.error('showReading 错误:', error);
    }
}

// 初始化所有事件（只执行一次）
function init() {
    if (isInitialized) {
        console.log('已初始化，跳过');
        return;
    }
    
    isInitialized = true;
    console.log('塔罗牌测试开始初始化...');
    
    // 等待 DOM 加载完成
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            setupEventListeners();
        });
    } else {
        setupEventListeners();
    }
}

// 设置事件监听器
function setupEventListeners() {
    try {
        console.log('设置事件监听器...');
        
        // 开始按钮
        const startBtn = document.getElementById('start-btn');
        if (startBtn) {
            startBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                console.log('点击开始抽牌');
                showPage('select-page');
                setTimeout(() => {
                    renderFanCards();
                }, 100);
            });
        }
        
        // 确认按钮
        const confirmBtn = document.getElementById('confirm-select-btn');
        if (confirmBtn) {
            confirmBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                handleConfirmSelect();
            });
        }
        
        // 解锁按钮
        const unlockBtn = document.getElementById('unlock-btn');
        if (unlockBtn) {
            unlockBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                if (adConfig.enabled) {
                    console.log('显示广告:', adConfig.adUnitId);
                } else {
                    console.log('测试模式：直接解锁');
                }
                showReading();
            });
        }
        
        // 跳过按钮
        const skipBtn = document.getElementById('skip-btn');
        if (skipBtn) {
            skipBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                showReading();
            });
        }
        
        // 分享按钮
        const shareBtn = document.getElementById('share-btn');
        if (shareBtn) {
            shareBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                if (navigator.share) {
                    const cardNames = currentCards.map(c => `${c.name}${c.position === 'upright' ? '正位' : '逆位'}`).join(', ');
                    navigator.share({
                        title: '我的塔罗牌测试结果',
                        text: `我抽到了：${cardNames}\n\n快来试试你的塔罗牌指引吧！`,
                        url: window.location.href
                    }).catch(err => {
                        console.log('分享取消');
                    });
                } else {
                    const cardNames = currentCards.map(c => `${c.name}${c.position === 'upright' ? '正位' : '逆位'}`).join(', ');
                    const shareText = `我抽到了：${cardNames}\n\n塔罗牌测试链接：${window.location.href}`;
                    
                    navigator.clipboard.writeText(shareText).then(() => {
                        alert('✅ 结果已复制到剪贴板！\n\n可以粘贴分享给朋友了~');
                    }).catch(() => {
                        alert('分享功能开发中...');
                    });
                }
            });
        }
        
        // 重新开始按钮
        const restartBtn = document.getElementById('restart-btn');
        if (restartBtn) {
            restartBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                if (confirm('确定要重新抽牌吗？')) {
                    selectedCards = [];
                    currentCards = [];
                    showPage('home-page');
                }
            });
        }
        
        console.log('事件监听器设置完成');
        console.log('塔罗牌测试初始化完成！');
    } catch (error) {
        console.error('setupEventListeners 错误:', error);
    }
}

// 启动初始化
init();

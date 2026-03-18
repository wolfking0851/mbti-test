// 抽牌逻辑

// 78 张塔罗牌数据
const tarotDeck = [
    // 大阿卡纳 (0-21)
    { id: 0, name: '愚人', nameEn: 'The Fool', image: 'cards/major/00_fool.jpg' },
    { id: 1, name: '魔术师', nameEn: 'The Magician', image: 'cards/major/01_magician.jpg' },
    { id: 2, name: '女祭司', nameEn: 'The High Priestess', image: 'cards/major/02_high_priestess.jpg' },
    { id: 3, name: '皇后', nameEn: 'The Empress', image: 'cards/major/03_empress.jpg' },
    { id: 4, name: '皇帝', nameEn: 'The Emperor', image: 'cards/major/04_emperor.jpg' },
    { id: 5, name: '教皇', nameEn: 'The Hierophant', image: 'cards/major/05_hierophant.jpg' },
    { id: 6, name: '恋人', nameEn: 'The Lovers', image: 'cards/major/06_lovers.jpg' },
    { id: 7, name: '战车', nameEn: 'The Chariot', image: 'cards/major/07_chariot.jpg' },
    { id: 8, name: '力量', nameEn: 'Strength', image: 'cards/major/08_strength.jpg' },
    { id: 9, name: '隐士', nameEn: 'The Hermit', image: 'cards/major/09_hermit.jpg' },
    { id: 10, name: '命运之轮', nameEn: 'Wheel of Fortune', image: 'cards/major/10_wheel.jpg' },
    { id: 11, name: '正义', nameEn: 'Justice', image: 'cards/major/11_justice.jpg' },
    { id: 12, name: '倒吊人', nameEn: 'The Hanged Man', image: 'cards/major/12_hanged_man.jpg' },
    { id: 13, name: '死神', nameEn: 'Death', image: 'cards/major/13_death.jpg' },
    { id: 14, name: '节制', nameEn: 'Temperance', image: 'cards/major/14_temperance.jpg' },
    { id: 15, name: '恶魔', nameEn: 'The Devil', image: 'cards/major/15_devil.jpg' },
    { id: 16, name: '高塔', nameEn: 'The Tower', image: 'cards/major/16_tower.jpg' },
    { id: 17, name: '星星', nameEn: 'The Star', image: 'cards/major/17_star.jpg' },
    { id: 18, name: '月亮', nameEn: 'The Moon', image: 'cards/major/18_moon.jpg' },
    { id: 19, name: '太阳', nameEn: 'The Sun', image: 'cards/major/19_sun.jpg' },
    { id: 20, name: '审判', nameEn: 'Judgement', image: 'cards/major/20_judgement.jpg' },
    { id: 21, name: '世界', nameEn: 'The World', image: 'cards/major/21_world.jpg' },
    
    // 权杖组 (22-35)
    { id: 22, name: '权杖 Ace', nameEn: 'Ace of Wands', image: 'cards/minor/wands_ace.jpg' },
    { id: 23, name: '权杖 2', nameEn: 'Two of Wands', image: 'cards/minor/wands_02.jpg' },
    { id: 24, name: '权杖 3', nameEn: 'Three of Wands', image: 'cards/minor/wands_03.jpg' },
    { id: 25, name: '权杖 4', nameEn: 'Four of Wands', image: 'cards/minor/wands_04.jpg' },
    { id: 26, name: '权杖 5', nameEn: 'Five of Wands', image: 'cards/minor/wands_05.jpg' },
    { id: 27, name: '权杖 6', nameEn: 'Six of Wands', image: 'cards/minor/wands_06.jpg' },
    { id: 28, name: '权杖 7', nameEn: 'Seven of Wands', image: 'cards/minor/wands_07.jpg' },
    { id: 29, name: '权杖 8', nameEn: 'Eight of Wands', image: 'cards/minor/wands_08.jpg' },
    { id: 30, name: '权杖 9', nameEn: 'Nine of Wands', image: 'cards/minor/wands_09.jpg' },
    { id: 31, name: '权杖 10', nameEn: 'Ten of Wands', image: 'cards/minor/wands_10.jpg' },
    { id: 32, name: '权杖侍从', nameEn: 'Page of Wands', image: 'cards/minor/wands_page.jpg' },
    { id: 33, name: '权杖骑士', nameEn: 'Knight of Wands', image: 'cards/minor/wands_knight.jpg' },
    { id: 34, name: '权杖王后', nameEn: 'Queen of Wands', image: 'cards/minor/wands_queen.jpg' },
    { id: 35, name: '权杖国王', nameEn: 'King of Wands', image: 'cards/minor/wands_king.jpg' },
    
    // 圣杯组 (36-49)
    { id: 36, name: '圣杯 Ace', nameEn: 'Ace of Cups', image: 'cards/minor/cups_ace.jpg' },
    { id: 37, name: '圣杯 2', nameEn: 'Two of Cups', image: 'cards/minor/cups_02.jpg' },
    { id: 38, name: '圣杯 3', nameEn: 'Three of Cups', image: 'cards/minor/cups_03.jpg' },
    { id: 39, name: '圣杯 4', nameEn: 'Four of Cups', image: 'cards/minor/cups_04.jpg' },
    { id: 40, name: '圣杯 5', nameEn: 'Five of Cups', image: 'cards/minor/cups_05.jpg' },
    { id: 41, name: '圣杯 6', nameEn: 'Six of Cups', image: 'cards/minor/cups_06.jpg' },
    { id: 42, name: '圣杯 7', nameEn: 'Seven of Cups', image: 'cards/minor/cups_07.jpg' },
    { id: 43, name: '圣杯 8', nameEn: 'Eight of Cups', image: 'cards/minor/cups_08.jpg' },
    { id: 44, name: '圣杯 9', nameEn: 'Nine of Cups', image: 'cards/minor/cups_09.jpg' },
    { id: 45, name: '圣杯 10', nameEn: 'Ten of Cups', image: 'cards/minor/cups_10.jpg' },
    { id: 46, name: '圣杯侍从', nameEn: 'Page of Cups', image: 'cards/minor/cups_page.jpg' },
    { id: 47, name: '圣杯骑士', nameEn: 'Knight of Cups', image: 'cards/minor/cups_knight.jpg' },
    { id: 48, name: '圣杯王后', nameEn: 'Queen of Cups', image: 'cards/minor/cups_queen.jpg' },
    { id: 49, name: '圣杯国王', nameEn: 'King of Cups', image: 'cards/minor/cups_king.jpg' },
    
    // 宝剑组 (50-63)
    { id: 50, name: '宝剑 Ace', nameEn: 'Ace of Swords', image: 'cards/minor/swords_ace.jpg' },
    { id: 51, name: '宝剑 2', nameEn: 'Two of Swords', image: 'cards/minor/swords_02.jpg' },
    { id: 52, name: '宝剑 3', nameEn: 'Three of Swords', image: 'cards/minor/swords_03.jpg' },
    { id: 53, name: '宝剑 4', nameEn: 'Four of Swords', image: 'cards/minor/swords_04.jpg' },
    { id: 54, name: '宝剑 5', nameEn: 'Five of Swords', image: 'cards/minor/swords_05.jpg' },
    { id: 55, name: '宝剑 6', nameEn: 'Six of Swords', image: 'cards/minor/swords_06.jpg' },
    { id: 56, name: '宝剑 7', nameEn: 'Seven of Swords', image: 'cards/minor/swords_07.jpg' },
    { id: 57, name: '宝剑 8', nameEn: 'Eight of Swords', image: 'cards/minor/swords_08.jpg' },
    { id: 58, name: '宝剑 9', nameEn: 'Nine of Swords', image: 'cards/minor/swords_09.jpg' },
    { id: 59, name: '宝剑 10', nameEn: 'Ten of Swords', image: 'cards/minor/swords_10.jpg' },
    { id: 60, name: '宝剑侍从', nameEn: 'Page of Swords', image: 'cards/minor/swords_page.jpg' },
    { id: 61, name: '宝剑骑士', nameEn: 'Knight of Swords', image: 'cards/minor/swords_knight.jpg' },
    { id: 62, name: '宝剑王后', nameEn: 'Queen of Swords', image: 'cards/minor/swords_queen.jpg' },
    { id: 63, name: '宝剑国王', nameEn: 'King of Swords', image: 'cards/minor/swords_king.jpg' },
    
    // 星币组 (64-77)
    { id: 64, name: '星币 Ace', nameEn: 'Ace of Pentacles', image: 'cards/minor/pentacles_ace.jpg' },
    { id: 65, name: '星币 2', nameEn: 'Two of Pentacles', image: 'cards/minor/pentacles_02.jpg' },
    { id: 66, name: '星币 3', nameEn: 'Three of Pentacles', image: 'cards/minor/pentacles_03.jpg' },
    { id: 67, name: '星币 4', nameEn: 'Four of Pentacles', image: 'cards/minor/pentacles_04.jpg' },
    { id: 68, name: '星币 5', nameEn: 'Five of Pentacles', image: 'cards/minor/pentacles_05.jpg' },
    { id: 69, name: '星币 6', nameEn: 'Six of Pentacles', image: 'cards/minor/pentacles_06.jpg' },
    { id: 70, name: '星币 7', nameEn: 'Seven of Pentacles', image: 'cards/minor/pentacles_07.jpg' },
    { id: 71, name: '星币 8', nameEn: 'Eight of Pentacles', image: 'cards/minor/pentacles_08.jpg' },
    { id: 72, name: '星币 9', nameEn: 'Nine of Pentacles', image: 'cards/minor/pentacles_09.jpg' },
    { id: 73, name: '星币 10', nameEn: 'Ten of Pentacles', image: 'cards/minor/pentacles_10.jpg' },
    { id: 74, name: '星币侍从', nameEn: 'Page of Pentacles', image: 'cards/minor/pentacles_page.jpg' },
    { id: 75, name: '星币骑士', nameEn: 'Knight of Pentacles', image: 'cards/minor/pentacles_knight.jpg' },
    { id: 76, name: '星币王后', nameEn: 'Queen of Pentacles', image: 'cards/minor/pentacles_queen.jpg' },
    { id: 77, name: '星币国王', nameEn: 'King of Pentacles', image: 'cards/minor/pentacles_king.jpg' },
];

/**
 * 从 78 张牌中随机抽取 3 张（不重复）
 * @returns {Array} 三张牌的数据，包含正逆位信息
 */
function drawCards() {
    // 洗牌算法（Fisher-Yates）
    const shuffled = [...tarotDeck];
    for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    
    // 抽取前三张
    const drawnCards = shuffled.slice(0, 3);
    
    // 为每张牌随机分配正逆位（50% 概率）
    return drawnCards.map(card => ({
        ...card,
        position: Math.random() > 0.5 ? 'upright' : 'reversed',
        positionName: Math.random() > 0.5 ? '正位' : '逆位'
    }));
}

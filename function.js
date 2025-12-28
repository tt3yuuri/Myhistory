// 雪が降るアニメーション
/*const dropSnowAnim = (option) => {
	// default option
	let default_option = {
		target_element: 'body', // taget HTML element
		where_to_insert: '', // Insert after the specified element in target_element. If unspecified, insert at the end of the target_element. ('img' 'p' '#id' etc)
		snow_amount: 5, // Amount of snow (min 1 max 10)
		snow_speed: 5, // Speed of snow (min 1 max 10)
		snow_color: '#FFF', // Color of snow (hex, rgba, name)
		snow_accumulation: true, // Whether or not there is snow accumulation.
		snow_emission_of_light: true, // Emission of light from snow.
		animation_time: 600 // Animation time (s)
	};

	// merge option
	let op = Object.assign(default_option, option);

	// whether the target element exists
	if (!document.querySelector(op.target_element)) {
		console.log('no target element.');
		return;
	}

	// target element
	let target_element = document.querySelector(op.target_element);
	target_element.style.position = 'relative';
	//target_element.style.overflow = 'hidden';

	// Insert after the specified element
	let insert_after_element = '';
	if (op.where_to_insert != '') {
		insert_after_element = target_element.querySelector(op.where_to_insert);
	}

	// main container
	let container = document.createElement('div');
	if (!insert_after_element) {
		target_element.appendChild(container);
	} else {
		insert_after_element.after(container);
	}
	container.style.position = 'absolute';
	container.style.top = 0;
	container.style.left = 0;
	container.style.width = '100%';
	container.style.height = '100%';
	container.style.overflow = 'visible';

	// snow container
	let snow_container = document.createElement('div');
	container.appendChild(snow_container);
	snow_container.style.position = 'absolute';
	snow_container.style.width = '100%';
	snow_container.style.height = '100%';

	// snow clone
	let snow = document.createElement('div');
	snow.style.position = 'absolute';
	snow.style.opacity = 0.8;
	snow.style.borderRadius = '50%';
	snow.style.backgroundColor = op.snow_color;

	let count = 0;
	op.animation_time *= 60;
	const update = () => {
		let rand1 = Math.floor(Math.random() * 100);
		let rand2 = Math.floor(Math.random() * 100);

		if (op.snow_accumulation == true) {
			snow_down_top = rand2;
		} else {
			snow_down_top = rand2 * 3;
		}

		if (count % (8 - op.snow_amount) == 0) {
			// snow
			let snow_clone = snow.cloneNode();
			snow_clone.style.width = `${0.02 * rand2}vw`;
			snow_clone.style.height = `${0.02 * rand2}vw`;
			snow_clone.style.left = `${rand1}%`;
			if (op.snow_emission_of_light == true) {
				snow_clone.style.boxShadow = `0 0 1vw 0.5vw rgba(255, 255, 255, 0.6)`;
			}
			snow_container.appendChild(snow_clone);

			let snow_anim = snow_clone.animate(
				[
					{ offset: 0, top: `-3vw` },
					{ offset: 1, top: `${rand2}%` }
				],
				{
					fill: 'forwards',
					duration: 25000 / op.snow_speed
				}
			);

			snow_anim.onfinish = (event) => {
				if (op.snow_accumulation == true) {
					setTimeout(() => {
						snow_clone.remove();
					}, 1000 * 60);
				} else {
					snow_clone.remove();
				}
			};
		}

		// stop or run animation
		count++;
		if (op.animation_time >= count) {
			requestAnimationFrame(update);
		} else {
			cancelAnimationFrame(update);
		}
	};

	update();
};

//////////////////////////// call function

let option = {
	target_element: '#snow', // taget HTML element
	where_to_insert: 'head', // Insert after the specified element in target_element. If unspecified, insert at the end of the target_element. ('img' 'p' '#id' etc)
	snow_amount: 3, // Amount of snow (min 1 max 10)
	snow_speed: 5, // Speed of snow (min 1 max 10)
	snow_color: '#eae9e9ff', // Color of snow (hex, rgba, name)
	snow_accumulation: false, // Whether or not there is snow accumulation.
	snow_emission_of_light: true, // Emission of light from snow.
	animation_time: 600 // Animation time (s)
};

dropSnowAnim(option);*/

// アイコンを降らせるアニメーション

document.addEventListener("DOMContentLoaded", () => {
    createSnowflakes();
});

function createSnowflakes() {
    // 1. 雪を入れるコンテナを作成してbodyに追加
    const snowContainer = document.createElement('div');
    snowContainer.id = 'snow-container';
    document.body.appendChild(snowContainer);

    // ⚡️ 設定：雪の数（増やしすぎると重くなるので注意）
    const numberOfFlakes = 50; 

    for (let i = 0; i < numberOfFlakes; i++) {
        // Font Awesomeのアイコン要素を作成
        const flake = document.createElement('i');
        
        // 2種類の結晶をランダムに混ぜる（fa-solid と fa-regular）
        //const iconType = Math.random() > 0.5 ? 'fa-solid' : 'fa-regular';
		const iconType = "fa-solid"; //本のアイコンがregularに対応していないため、solidに固定
        
        let iconName;
		let kakuritu = Math.random()
		
		if(kakuritu < 0.2) { // 0.3を変えると出現率の変更ができる（0.3→30%）
			iconName = "fa-star";
			flake.classList.add("falling-star"); //☆専用のクラスに追加
		} else if(kakuritu < 0.3) {
			iconName = "fa-book";
			flake.classList.add("falling-book");
		} else {
			iconName = "fa-snowflake";
		}

		flake.classList.add(iconType, iconName, "falling-snow")

        // 横位置（画面の左端0%から右端100%の間）
        flake.style.left = Math.random() * 100 + 'vw';
        
        // 大きさ（10px から 25px の間）
        const size = Math.random() * 30 + 20;
        flake.style.fontSize = size + 'px';
        
        // 落ちる速度（アニメーション時間：5秒 から 15秒 の間）
        const duration = Math.random() * 10 + 5;
        flake.style.animationDuration = duration + 's';

        // 開始の遅延（これがないと一斉に降り始めて不自然になる）
        // 0秒から開始までの間にランダムにスタートさせる
        flake.style.animationDelay = -Math.random() * duration + 's';

        // 透明度をランダムにして奥行き感を出す
        flake.style.opacity = Math.random() * 0.6 + 0.4;

        // コンテナに結晶を追加
        snowContainer.appendChild(flake);
    }
}
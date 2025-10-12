// 雪が降るアニメーション
const dropSnowAnim = (option) => {
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

dropSnowAnim(option);

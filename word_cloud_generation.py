from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Extract words from descriptions
descriptions = """Two elephants walking on dusty road.
Two cute cats peacefully resting on a red blanket on a bed.
Three giraffes standing on a dusty road in the wilderness.
Two dogs sitting on wooden railing looking out.
A group of baby sea turtles swimming gracefully in the water.
Three geese gracefully gliding on water.
Majestic tiger perched on a grassy rock.
Group of camels resting in Wadi Rum desert.
Two green lizards perched on a branch.
Two flamingos forming a heart shape with their beaks.
Two hippopotamus swimming in river.
Three cute white kittens snuggled in a person's lap.
Playful polar bear cub exploring the icy terrain.
A group of monkeys sitting closely together in a natural setting.
A macaque monkey stands on green grass with a baby monkey clinging to its back. The adult monkey is holding a piece of yellow fruit in one hand.
Two men in traditional white attire sit on the ground, facing each other, with their backs to the camera at a cultural event. In the background, richly decorated camels with colorful saddles and tassels stand amidst a crowd of attendees. The sky is clear blue.
a close up of a bird
Five adorable kittens standing together on a lush green grassy field.
A deceased alligator floating in the water.
two rhinos grazing on a dirt road
a woman standing in front of a large fish tank
Two lemurs perched on a ledge, one gazing into the distance while the other looks curiously at the camera.
a dolphin swimming in the water
a horse standing in a snowy field
Graceful white ducks enjoying the green grass.
Three curious cows with ear tags standing in a sunny field against a clear blue sky.
a group of sheep in a barn
Green chameleon perched on a branch.
Group of bison grazing in a cloudy field.
Two majestic polar bears locking eyes in the Arctic.
A squirrel perched on a lush green field.
A vibrant yellow tang fish swimming next to a blue spotted reef fish in an aquarium with a coral reef background.
A brown antelope with spiral horns looking to the side, and a bird with a red beak standing on its back against a green foliage background.
Close-up of a Keel-billed Toucan with bright yellow chest, black body, and multicolored beak perched on a branch
a deer standing on dirt
a group of giraffes standing in a field
Two alpacas standing in a field under a clear blue sky.
a wolf lying down in the woods
Two meerkats standing in the wild, alert and curious, with their heads raised and bodies upright.
Two birds soaring gracefully through the sky, their wings outstretched in perfect harmony.
A fluffy yellow duckling sitting on the ground with its orange webbed feet stretched out in front.
a fox sitting on the ground
two guinea pigs with leaves
a group of zebras drinking water
Hippos swimming in a serene water body, showcasing their massive bodies and powerful presence.
A gentle touch between human and horse.
A couple of birds sitting on top of a tree branch
Two lions resting on each other, displaying affection and camaraderie in their peaceful slumber.
Two birds perched on a bird bath, one with colorful feathers and the other with a sleek black plumage.
Two brown bears engaged in a fierce battle in the water, showcasing their strength and dominance."""

words = " ".join(descriptions.split()[1::2])  # Extract every other word (the actual descriptions)
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(words)

# Display the generated word cloud using matplotlib
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
